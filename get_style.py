import requests
import json
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from urllib.parse import urljoin
import time

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
prompt = """Analyze the provided collection of articles and describe their:
1. Writing Style:
- Sentence structure (e.g., concise vs. elaborate, use of passive/active voice).
- Vocabulary (e.g., technical, colloquial, academic).
- Formality level (e.g., casual, professional, scholarly).
- Use of literary devices (e.g., metaphors, anecdotes, rhetorical questions).

2. Tone:
- Emotional undertones (e.g., authoritative, conversational, persuasive, neutral).
- Use of humor, sarcasm, or empathy.
- Consistency in tone across articles.

3. Article Characteristics:
- Use of evidence (e.g., data-driven, anecdotal, citation-heavy).
- Narrative voice (e.g., first-person, third-person, collective perspective).
- Structural patterns (e.g., headings, bullet points, call-to-actions).

4. Unique Distinguishing Features:
-Recurring phrases, formatting quirks, or stylistic trademarks.
-Balance between descriptive vs. prescriptive content.

Output Requirements:
-Summarize your findings into a clear, structured guide.
-Provide actionable guidelines for a new writer to replicate the style (e.g., “Use short paragraphs with subheadings for clarity,” “Avoid jargon; prioritize conversational phrasing”).
-Highlight any dos/don’ts or pitfalls to avoid.

Articles:
---
{docs}
---
Response: """
prompt = PromptTemplate(template=prompt,
                        input_variables=["title", "tags", "body"],
                        )

chain = prompt | llm

json_parser = JsonOutputParser()
ref_path_json = "jenosize_articles_ref_new.jsonl"

# read the articles to list
data = []
with open('jenosize_articles_ref.jsonl', 'r') as file:
    for line in file:
        data.append(json.loads(line))

# join the list of articles into a single string
docs = "\n---\n".join([f"Title: {article['title']}\nTags: {article['tags']}\nBody: {article['body']}" for article in data])
response = chain.invoke({"docs": docs})

print(response.content)

# save the response (article style) to a file
with open("article_style.txt", 'w') as f:
    f.write(response.content)
        