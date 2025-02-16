import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import PyPDF2
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
import nest_asyncio

# Initialize LangChain with OpenAI's Chat API
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
json_parser = JsonOutputParser()
article_tags = ["-", "Technology", "Art", "Motivation", "Selfcare", "Food", "Business", "Nature", "Marketing"]

with open("article_style_commend.txt", "r") as file:
    guidelines = file.read()

# Define the prompt template for generating topics
topic_prompt_template = """Generate a relevant and engaging topic title and description for a business article following these guidelines:
- The topic should be related to {industry} and aimed at being relevant with {target_audience}.
- The description should provide a brief overview of the topic and provide a detailed article structure plan (e.g., introduction, key points).
- Do not mention {target_audience} directly in the topic.
- Your structure should be clear and concise, focusing on the main points.
- Do not add a conclusion secction in the structure plan.

Respond in the following JSON format:
{{
    "topic": <generated topic>,
    "description": <brief description of the topic>
}}
"""
topic_prompt = PromptTemplate(
    input_variables=["industry", "target_audience"],
    template=topic_prompt_template
)

# Define the prompt template for generating articles
article_prompt_template = """Web Document: {web_docs}
---
Documents: {pdf}
---
As a business trend analyst, generate a detailed article with `{topic}` as an article name with the following conditions:
- The article must follow these given characteristics: {description}.
- Include perspectives about future trends and ideas for businesses in the {industry} industry.
- Cater to {target_audience} perspective but avoid mention {target_audience} directly.
- Use data and insights from source and document to support your analysis.
- Your article must follow the guidelines provided:
---
{guidelines}
---
Response: """
article_prompt = PromptTemplate(
    input_variables=["web_docs", "pdf", "topic", "description", "industry", "target_audience", "guidelines"],
    template=article_prompt_template
)

# Create the LLM chains
topic_chain = topic_prompt | llm | json_parser
trend_chain = article_prompt | llm

# Function to generate a topic
def generate_topic(industry1, industry2, industry3, target_audience):
    industries = [industry for industry in [industry1, industry2, industry3] if industry != "-"]
    topic = topic_chain.invoke({
        "industry": ", ".join(industries),
        "target_audience": target_audience
    })
    return topic['topic'], topic['description']

# Function to extract text from PDF (supports both local files and UploadFile objects)
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        # Check if pdf_file has a 'file' attribute (as in FastAPI's UploadFile or Gradio's file)
        if hasattr(pdf_file, "file"):
            reader = PyPDF2.PdfReader(pdf_file.file)
        else:
            with open(pdf_file.name, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        text = ""
    return text

# Function to scrape text from a URL
def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

# Gradio interface function for generating articles
def generate_article(topic_category, description, industry1, industry2, industry3, target_audience, pdf, url):
    try:
        pdf_text = extract_text_from_pdf(pdf) if pdf else ""
    except Exception as e:
        pdf_text = ""
        
    try:
        url_text = scrape_text_from_url(url)
    except Exception as e:
        url_text = ""
    
    industries = [industry for industry in [industry1, industry2, industry3] if industry != "-"]

    raw_article = trend_chain.invoke({
        "web_docs": url_text,
        "pdf": pdf_text,
        "topic": topic_category,
        "description": description,
        "industry": ", ".join(industries),
        "target_audience": target_audience,
        "guidelines": guidelines,
    })
    result = raw_article.content
    return result

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Jenosize Assignment: Article Generator")
    with gr.Row():
        with gr.Column():
            industry_dropdown_1 = gr.Dropdown(
                choices=article_tags,
                label="Industry 1",
                value="-"
            )
            industry_dropdown_2 = gr.Dropdown(
                choices=article_tags,
                label="Industry 2",
                value="-"
            )
            industry_dropdown_3 = gr.Dropdown(
                choices=article_tags,
                label="Industry 3",
                value="-"
            )
            target_audience_dropdown = gr.Dropdown(
                choices=["Executives", "Entrepreneurs", "Developers", "Marketers", "Students"],
                label="Target Audience",
                value="Executives"
            )
            topic_textbox = gr.Textbox(lines=2, label="Article Title", placeholder="Article title")
            description_textbox = gr.Textbox(lines=2, label="Description", placeholder="Specify what and how you would like the article to be written")
            auto_generate_button = gr.Button("Auto Generate Topic using `Industry` and `Target Audience`")
        with gr.Column():
            pdf_upload = gr.File(label="Upload PDF", file_types=[".pdf"])
            urls_input = gr.Textbox(
                lines=1,
                placeholder="Enter the URLs of the articles you want to use as references",
                label="URLs"
            )
    auto_generate_button.click(
        generate_topic,
        inputs=[industry_dropdown_1, industry_dropdown_2, industry_dropdown_3, target_audience_dropdown],
        outputs=[topic_textbox, description_textbox]
    )
    generate_button = gr.Button("Generate Article")
    plain_text_output = gr.Textbox(label="Generated Article", interactive=False)
    generate_button.click(
        generate_article,
        inputs=[
            topic_textbox,
            description_textbox,
            industry_dropdown_1,
            industry_dropdown_2,
            industry_dropdown_3,
            target_audience_dropdown,
            pdf_upload,
            urls_input
        ],
        outputs=plain_text_output
    )

# ---------------- FastAPI Integration ---------------- #

app = FastAPI()

@app.get("/")
async def generate_topic_endpoint():
    return {"message": "Welcome to the Jenosize Assignment Article Generator! \
        Please use the /generate_topic and /generate_article endpoints to generate topics and articles. \
            Check the /gradio endpoint for the Gradio interface and /docs for the API documentation."}

@app.post("/generate_topic")
async def generate_topic_endpoint(
    industry1: str = Form(...),
    industry2: str = Form(...),
    industry3: str = Form(...),
    target_audience: str = Form(...)
):
    topic, description = generate_topic(industry1, industry2, industry3, target_audience)
    return {"topic": topic, "description": description}

@app.post("/generate_article")
async def generate_article_endpoint(
    topic_category: str = Form(...),
    description: str = Form(...),
    industry1: str = Form(...),
    industry2: str = Form(...),
    industry3: str = Form(...),
    target_audience: str = Form(...),
    url: str = Form(...),
    pdf: UploadFile = File(None)
):
    pdf_text = extract_text_from_pdf(pdf) if pdf else ""
    try:
        url_text = scrape_text_from_url(url)
    except Exception as e:
        url_text = ""
    
    industries = [industry for industry in [industry1, industry2, industry3] if industry != "-"]
    raw_article = trend_chain.invoke({
        "web_docs": url_text,
        "pdf": pdf_text,
        "topic": topic_category,
        "description": description,
        "industry": ", ".join(industries),
        "target_audience": target_audience,
        "guidelines": guidelines,
    })
    return {"article": raw_article.content}

# Mount the Gradio app at the /gradio endpoint
app = gr.mount_gradio_app(app, demo, path="/gradio")

if __name__ == "__main__":
    nest_asyncio.apply()  # Allows nested event loops if running in an async environment
    uvicorn.run(app, host="0.0.0.0", port=8000)
