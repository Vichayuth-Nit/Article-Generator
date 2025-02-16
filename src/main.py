import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import PyPDF2
import requests
from bs4 import BeautifulSoup

# Initialize LangChain with OpenAI's Chat API
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
json_parser = JsonOutputParser()
article_tags = ["-",'Technology', 'Art', 'Motivation', 'Selfcare', 'Food', 'Business', 'Nature', 'Marketing']
with open("article_style_commend.txt", "r") as file:
    guidelines = file.read()

# Define the prompt template for generating topics
topic_prompt_template = """Generate a relevant and engaging topic title and description for a business article following these guidelines:
- The topic should be related to {industry} and aimed at being relevant with {target_audience}.
- The description should provide a brief overview of the topic and provide a detailed article structure plan (e.g., introduction, key points).
- Do not mention {target_audience} directly in the topic.
- Your structure should be clear and concise, focusing on the main points.
- Do not make a conclusion in the structure plan.

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

# Function to extract text from PDF (updated for PyPDF2 3.x+)
def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file.name, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to scrape text from a URL
def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

# Gradio interface function
def generate_article(topic_category, description, industry1, industry2, industry3, target_audience, pdf, url):
    # Extract text from PDF
    try:
        pdf_text = extract_text_from_pdf(pdf) if pdf else ""
    except:
        pdf_text = ""
        
    # Extract text from url
    try:
        url_text = scrape_text_from_url(url)
    except:
        url_text = ""

    industries = [industry for industry in [industry1, industry2, industry3] if industry != "-"]

    # Generate the article using LangChain
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

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Jenosize assignment: Article Generator")
    
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
            topic_textbox = gr.Textbox(lines=2, label="Article title", placeholder="article title")
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

demo.launch()