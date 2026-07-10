from openai import OpenAI

from app.core.config import settings


client = OpenAI(api_key=settings.openai_api_key)


def answer_with_context(question: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)

    prompt = f"""
You are a mortgage lender guideline assistant.

Format the answer well with proper space between lists.

Use only the provided lender guideline context to answer the user's question.
If the context does not contain enough information, say that clearly.
Do not make final lending decisions. Present likely matches and explain why.
Do not add an explanation saying you are not making final decisions.


Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text