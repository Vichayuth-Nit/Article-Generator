### Report for Jenosize Assignment: Trend & Future Ideas Articles

#### Model Selection & Fine-Tuning

**Model Selection:**
For this project, I selected the GPT-4 model from OpenAI, specifically the "gpt-4o-mini" variant. This model is well-suited for generating high-quality, insightful articles due to its advanced language understanding, generation capabilities, and large context windows available for RAG.

**Fine-Tuning Process:**
The model was not finetune as I use prompt engineering to tackle and improve article quality instead. Firstly I scraped some Jenosize's content and metadata (get_article.py, jenosize_articles_ref.jsonl) and use llm as an analyzer to generate a writing guideline to simulate article's writting style while also filter out some of insignificant factor by myself (get_style.py, article_style.txt, article_style_commend.txt). Any given document will be used as context to improve the quality of the generated article.

**Challenges:**
One of the main challenges was ensuring the model's output remained consistent with Jenosize's professional and informative tone. This was addressed by carefully curating Jenosize's articles and implementing prompt templates that guide the model's responses to follow the writing guideline.

#### Data Engineering / Model Deployment / API Deployment
To handle the data pipeline issue and ease of end-user. I choose to deploy the model with Gradio which could both create a stylize frontend with FastAPI application intergrated in the same deploy. The API provides an endpoint where users can input a topic or parameter and receive a generated article in response.

**Endpoint:**
- **POST /generate_article**: Accepts input parameters such as topic title, topic description, industry, target audience, and other reference materials (web url, pdf), and returns a generated article. (More detail on http://127.0.0.1:8000/docs#/)


**Link to Test App Prototype:**
<reasoning why you don't understand>

**Conclusion:**
This project successfully demonstrates the ability to generate high-quality, insightful articles aligned with Jenosize's content style using a fine-tuned GPT-4 model. The deployment via FastAPI ensures the solution is accessible and scalable, providing a valuable tool for generating business trend articles.

---

**Note:** Some details such as the link to the test app prototype were not provided in the original assignment. If further clarification is needed, please let me know.