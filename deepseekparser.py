import re
from langchain.schema import BaseOutputParser


class DeepSeekParser(BaseOutputParser):

    def parse(self, text: str) -> str:
        cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        cleaned_text = re.sub(r"\*\*", "", cleaned_text, flags=re.DOTALL)
        return cleaned_text.strip()
