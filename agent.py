from langchain_community.document_loaders import YoutubeLoader
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import argparse
import logging

logger = logging.getLogger(__name__)


class YoutubeSummaryAgent:

    def __init__(self, model_name="llama3.2:1b"):
        self.model = OllamaLLM(model=model_name, temprature=0)
        logger.info(f"{model_name} model is loaded")
        self.template = """
        As an expert copywriter, your job is to create a point wise summary of the following transcript in simple to understand language.
        Your response should be only the summary.
        Transcript:{transcript}
        """
        self.prompt = PromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    def summarize(self, url):
        self.is_valid_youtube_url(url)
        if self.is_valid_youtube_url(url):
            loader = YoutubeLoader.from_youtube_url(url)
            documents = loader.load()
            response = self.chain.invoke({"transcript": documents[0].page_content})
        else:
            response = "Invalid Youtube URL"
        return response

    def is_valid_youtube_url(self, url):
        import re

        youtube_regex = re.compile(
            r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+"
        )
        return youtube_regex.match(url)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    load_dotenv()

    parser = argparse.ArgumentParser(description="Youtube Summarizer")
    parser.add_argument("--url", type=str, help="youtube url")
    args = parser.parse_args()

    assert args.url is not None, "You must provide a YouTube URL."

    model_name = os.getenv("MODEL")
    agent = YoutubeSummaryAgent(model_name=model_name)
    summary = agent.summarize(args.url)

    print(summary)
