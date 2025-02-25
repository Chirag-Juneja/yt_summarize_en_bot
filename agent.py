import os
import argparse
import logging
from langchain_ollama.llms import OllamaLLM
from langchain_community.document_loaders import YoutubeLoader
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from deepseekparser import DeepSeekParser
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


logger = logging.getLogger(__name__)


class Agent:

    def __init__(self, model_name="deepseek-r1:1.5b"):
        self.model = OllamaLLM(model=model_name, temprature=0)
        logger.info(f"{model_name} model is loaded")
        self.template = """
        As an expert copywriter, your job is to create a point wise summary of the following transcript in simple to understand language.
        Your response should be only the summary.
        Your response should not exceed 4096 characters.
        Transcript:{transcript}
        """
        self.prompt = PromptTemplate.from_template(self.template)
        self.output_parser = DeepSeekParser()
        self.chain = self.prompt | self.model | self.output_parser

    def chunk_docs(self, docs):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=64000, chunk_overlap=4000, add_start_index=True
        )
        return splitter.split_documents(docs)

    def summarize(self, doc):
        response = self.chain.invoke({"transcript": doc})
        return response

    def __call__(self, url):
        self.is_valid_youtube_url(url)
        if self.is_valid_youtube_url(url):
            loader = YoutubeLoader.from_youtube_url(url)
            docs = loader.load()
            summaries = []
            chunks = self.chunk_docs(docs)
            if len(chunks) > 1:
                for chunk in chunks:
                    summaries.append(self.summarize(chunk))
                response = self.summarize(Document(page_content=" ".join(summaries)))
            else:
                response = self.summarize(docs[0])
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
    agent = Agent(model_name=model_name)
    # summary = agent.summarize(args.url)
    summary = agent(args.url)

    print(summary)
