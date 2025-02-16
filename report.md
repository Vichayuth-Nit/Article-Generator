## Report for Jenosize Assignment: Trend & Future Ideas Articles
#### By Vichayuth Nitayasomboon

#### Model Selection
For this project, I selected the GPT-4 model from OpenAI, specifically the "gpt-4o-mini" variant. This model is well-suited for generating high-quality, insightful articles due to its advanced language understanding, generation capabilities, and large context windows available for RAG.

---

#### Prompt Engineering process
The model was not finetune as I use prompt engineering to tackle and improve article quality instead. Firstly I scraped some Jenosize's content and metadata (get_article.py, jenosize_articles_ref.jsonl) and use llm as an analyzer to generate a writing guideline to simulate article's writting style. After that, I filter out some of insignificant factor from the writing guideline by myself (get_style.py, article_style.txt, article_style_commend.txt). Any given document will be used as context to improve the quality of the generated article.

---

#### Challenges
One of the main challenges was ensuring the model's output remained consistent with Jenosize's professional and informative tone. This was addressed by carefully curating Jenosize's articles and implementing prompt templates that guide the model's responses to follow the writing guideline.

---

#### Data Engineering / Model Deployment / API Deployment
To handle the data pipeline issue and ease of end-user. I choose to deploy the model with Gradio in HuggingFace Space which could both create a stylize frontend with FastAPI application intergrated in the same deploy. The API provides an endpoint where users can input a topic or parameter and receive a generated article in response.

---

#### Important Endpoint
- **POST /generate_article**: Accepts input parameters such as topic title, topic description, industry, target audience, and other reference materials (web url, pdf), and returns a generated article. More detail on Swagger Document: http://127.0.0.1:8000/docs#/ (required cloning repo and opening gradio demo first)

---

#### Link to Test App Prototype
You can access the prototype here: https://huggingface.co/spaces/Vichayuth/Article-Generator-demo

---

#### Potential Improvement
- **AI-Powered Search Engine Tools**: Implement AI agents that can automatically search for and gather reference documents from various sources, increasing the number of reference materials available for article generation.
- **Automated Article Reviser/Translator**: Develop an AI agent capable of revising and enhancing the quality of generated articles. This agent could also translate articles into Thai, ensuring high-quality content in multiple languages.
- **Markdown Editor**: Create an AI agent that can convert generated articles into Markdown format, making them ready for deployment on various platforms with minimal manual editing.
- **Automated Image Generator**: Integrate an AI-based image generation tool that can create relevant images to accompany the articles, enhancing the visual appeal and engagement of the content.
- **Automated Article Voice Over generator**: Develop an AI agent that can generate voice overs for the articles. This feature could significantly improve the user experience for blind and disabled individuals by providing them with audio versions of the content, making it more accessible.

---

**Conclusion:**
This project successfully demonstrates the ability to generate high-quality, insightful articles aligned with Jenosize's content style using a GPT-4o-mini with prompt engineering method. The deployment via FastAPI/gradio_client ensures the solution is accessible both for End-user and developer with scalability, providing a valuable tool for generating business trend articles.

---