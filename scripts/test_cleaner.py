from backend.rag_engine.preprocessing.normalizer import Normalizer

normalizer = Normalizer()

text = """
“Hello”—World…
It's ２０２６.
"""

print(normalizer.normalize(text))