from openai import OpenAI

from app.core.config import settings


def create_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    if not settings.openai_api_key:
        raise RuntimeError(
            "An OpenAI API key is required to generate embeddings."
        )

    client = OpenAI(api_key=settings.openai_api_key)

    response = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
        dimensions=settings.embedding_dimensions,
    )

    return [item.embedding for item in response.data]