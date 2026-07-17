from rag_engine.chunking.splitter import Splitter


text = """
Hello World.

This is paragraph one.


This is paragraph two.

It has two sentences.
"""

splitter = Splitter()

print(splitter.split_paragraphs(text))

print("----------------")

print(splitter.split_sentences(text))