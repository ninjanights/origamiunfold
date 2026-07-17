from rag_engine.models.document import Document
from rag_engine.preprocessing.cleaner import Cleaner
from rag_engine.preprocessing.normalizer import Normalizer
from rag_engine.preprocessing.deduplicator import Deduplicator


class PreprocessingPipeline:
    def __init__(self):
        self.cleaner = Cleaner()
        self.normalizer = Normalizer()
        self.deduplicator = Deduplicator()

    def process(self, document: Document) -> Document:
        text = document.content
        text = self.cleaner.clean(text)
        text = self.normalizer.normalize(text)
        text = self.deduplicator.remove_duplicates(text)
        document.content = text

        return document
