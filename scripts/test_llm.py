from rag_engine.llm.llm_itself import LLMItself

llm = LLMItself()

ans = llm.generate("say hello in hiragana.")

print(ans)
