import requests
import json
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from urllib.parse import urljoin
import time

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
prompt = """Describe the given article writing style from the given infomation.\nTitle: {title}\nTags: {tags}\nBody: {body}
---
Avoid calling this article by it name, summarize at the end of the description."""
prompt = PromptTemplate(template=prompt,
                        input_variables=["title", "tags", "body"],
                        )

chain = prompt | llm

json_parser = JsonOutputParser()
ref_path_json = "jenosize_articles_ref_new.jsonl"

def scrape_text_from_url(url_list):
    broke_url = []
    for url in url_list:
        time.sleep(5)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # get article title, tags, and body
            title = soup.find('h1').get_text()
            tags = soup.select_one('div.lg\:flex.mt-5').get_text("\n", strip=True).split("\n")
            body = soup.find('div', class_='font-gtr content-detail-en content-detail txt-web-body mt-5 md:mt-11 max-w-7xl mx-auto px-5 text-lg').get_text("")
            
            # generate article description in case we want to use it
            description = chain.invoke({
                "title": title,
                "tags": tags,
                "body": body
            }).content
            
            json_body = json.dumps({
                "url": url,
                "title": title,
                "tags": tags,
                "body": body,
                "description": description
            })
            # print the article information
            print(url)
            print(title)
            print(tags)
            print(description)
            print('---')
            
            # save the article information to a json file
            with open(ref_path_json, 'a') as f:
                f.write(json_body + "\n")
        
    # handle error and exceptions by looping through the function again for the failed url
        except Exception as e:
            print(f"Error: {e}")
            broke_url.append(url)
            time.sleep(5)
            continue
    if broke_url:
        scrape_text_from_url(broke_url)


# a list of urls to scrape from `https://www.jenosize.com/en/ideas`
scrape_text_from_url(list({
    "https://www.jenosize.com/en/ideas/transformation-and-technology/fintech-trends",
    "https://www.jenosize.com/en/ideas/transformation-and-technology/technologies-for-real-estate",
    "https://www.jenosize.com/en/ideas/transformation-and-technology/omni-channel-for-retail-business",
    "https://www.jenosize.com/en/ideas/futurist/agentic-ai-guide-for-modern-business",
    "https://www.jenosize.com/en/ideas/futurist/behavioral-design-for-marketing",
    "https://www.jenosize.com/en/ideas/futurist/what-is-quantum-computing",
    "https://www.jenosize.com/en/ideas/futurist/thai-ai-service-platforms",
    "https://www.jenosize.com/en/ideas/understand-people-and-consumer/stp-marketing-strategy-guide",
    "https://www.jenosize.com/en/ideas/understand-people-and-consumer/5-dimensions-of-service-quality",
    "https://www.jenosize.com/en/ideas/understand-people-and-consumer/consumer-buying-roles-marketing-guide",
    "https://www.jenosize.com/en/ideas/understand-people-and-consumer/introducing-gen-beta",
    "https://www.jenosize.com/en/ideas/transformation-and-technology/crm-vs-cdp-differences",
    "https://www.jenosize.com/en/ideas/utility-for-our-world/carbon-credits-business-opportunities",
    "https://www.jenosize.com/en/ideas/utility-for-our-world/plant-based-food-business",
    "https://www.jenosize.com/en/ideas/utility-for-our-world/fast-fashion-trend",
    "https://www.jenosize.com/en/ideas/utility-for-our-world/regenerative-business",
    "https://www.jenosize.com/en/ideas/real-time-marketing/linkedin-marketing-strategy-guide",
    "https://www.jenosize.com/en/ideas/real-time-marketing/festive-marketing",
    "https://www.jenosize.com/en/ideas/real-time-marketing/omni-channel-vs-o2o-marketing",
    "https://www.jenosize.com/en/ideas/real-time-marketing/youtube-trends",
    "https://www.jenosize.com/en/ideas/experience-the-new-world/top-startup-trends",
    "https://www.jenosize.com/en/ideas/experience-the-new-world/oligopoly-market-in-thailand",
    "https://www.jenosize.com/en/ideas/experience-the-new-world/is-hybrid-working-the-new-norm",
    "https://www.jenosize.com/en/ideas/experience-the-new-world/top-ten-megatrends-in-2025",
}))