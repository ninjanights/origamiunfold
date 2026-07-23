import re

class Splitter:
    def split_paragraphs(self, text: str) -> list[str]:
        return [p for p in re.split(r"\r\n\s*\n", text)  if p.strip()  ]
    
    def split_lines(self, text:str) -> list[str]:
        return [line for line in text.splitlines() if line.strip()]

    def split_sentences(self, text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s for s in sentences if s.strip()]
    
    def split_words(self, text: str) -> list[str]:
        return text.split()

    