import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")
django.setup()


from backend.rag_engine.llm.llm_itself import LLMItself

llm = LLMItself()

ans = llm.generate("say hello in hiragana.")

print(ans)
