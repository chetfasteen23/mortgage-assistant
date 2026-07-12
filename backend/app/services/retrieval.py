from sqlalchemy.orm import Session

from app.models.lender_chunk import LenderChunk
from app.services.embeddings import create_embeddings


def search_lender_chunks(
    db: Session,
    question: str,
    limit: int = 5,
) -> list[LenderChunk]:
    question_embedding = create_embeddings([question])[0]

    return (
        db.query(LenderChunk)
        .filter(LenderChunk.embedding.is_not(None))
        .order_by(
            LenderChunk.embedding.cosine_distance(question_embedding)
        )
        .limit(limit)
        .all()
    )