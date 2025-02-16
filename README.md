## Setup and Run

1. Run the setup script:
    ```sh
    python setup.py
    ```

2. If the virtual environment is not activated automatically, activate it manually:
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```

3. Add your OpenAI API key to the environment variables:
    ```sh
    export OPENAI_API_KEY='your-api-key-here'
    ```

4. Run the main script to open the article generator demo:
    ```sh
    python src/main.py
    ```
    or run fastapi integrated version:
    ```sh
    uvicorn src.main_fastapi:app --reload
    ```
    For demo: go to http://127.0.0.1:8000/gradio
    For Swagger: go to http://127.0.0.1:8000/docs


## Code Explanation

### get_article.py
This script scrapes articles from the Jenosize website to use as references. It extracts the title, tags, and body of each article and stores them in a file named `jenosize_article_ref.jsonl`. The script uses BeautifulSoup to parse HTML content and the LangChain OpenAI API to generate descriptions of the articles. If any URLs fail to load, the script retries them after a short delay.

### get_style.py
This script uses a language model to analyze the overall article style and guidelines for producing articles in the same style as Jenosize. It reads the articles from `jenosize_article_ref.jsonl`, generates a style guide, and stores the results in `article_style.txt`. The style guide is then hand-labeled and saved in a new file named `article_style_commend.txt`.

### main.py and main_fastapi.py
This script runs the main application, which generates articles based on the style and guidelines determined by `get_style.py`. It uses the OpenAI API to generate content and demonstrates the article generation process. The script includes functions to generate topics, extract text from PDFs, and scrape text from URLs. It uses Gradio to create an interactive interface where users can input industry categories, target audiences, and reference materials to generate articles.

## Potential Improvement

- **AI-Powered Search Engine Tools**: Implement AI agents that can automatically search for and gather reference documents from various sources, increasing the number of reference materials available for article generation.
- **Automated Article Reviser/Translator**: Develop an AI agent capable of revising and enhancing the quality of generated articles. This agent could also translate articles into Thai, ensuring high-quality content in multiple languages.
- **Markdown Editor**: Create an AI agent that can convert generated articles into Markdown format, making them ready for deployment on various platforms with minimal manual editing.
- **Automated Image Generator**: Integrate an AI-based image generation tool that can create relevant images to accompany the articles, enhancing the visual appeal and engagement of the content.
