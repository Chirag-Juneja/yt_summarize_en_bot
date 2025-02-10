from langchain_community.document_loaders import YoutubeLoader
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import argparse


class YoutubeSummaryAgent:

    def __init__(self):
        self.model = OllamaLLM(model=os.getenv("MODEL"), temprature=0)
        self.template = """
        As an expert copywriter, your job is to create a point wise summary of the following transcript in simple to understand language.
        Your response should be only the summary.
        Transcript:{transcript}
        """
        self.prompt = PromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    def summarize(self, url):
        loader = YoutubeLoader.from_youtube_url(url)
        documents = loader.load()
        response = self.chain.invoke({"transcript": documents[0].page_content})
        return response


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Youtube Summarizer")
    parser.add_argument("--url", type=str, help="youtube url")
    args = parser.parse_args()

    agent = YoutubeSummaryAgent()
    summary = agent.summarize(args.url)

    print(summary)
