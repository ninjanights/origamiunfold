from rag_engine.models.chunk import Chunk


class PromptBuilder:
    def build(
        self,
        question: str,
        chunks: list[Chunk],
    ) -> str:
        context = "\n\n".join(chunk.content for chunk in chunks)

        prompt = f"""
        You are a helpful AI assistant.
        Answer ONLY from the provided context.
        If the answer is not present in the context, say:
        "I couldn't find that information in the provided documents."

        Context
        {context}.
        Question
        {question}.
        Answer:
        """
        return prompt.strip()