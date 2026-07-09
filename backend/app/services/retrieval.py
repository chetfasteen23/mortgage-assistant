from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.lender_chunk import LenderChunk


STOP_WORDS = {
    "which",
    "what",
    "who",
    "where",
    "when",
    "why",
    "how",
    "the",
    "a",
    "an",
    "with",
    "for",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "do",
    "does",
    "allow",
    "allows",
    "lender",
    "lenders",
}


def extract_keywords(question: str) -> list[str]:
    words = question.lower().replace("?", "").replace(",", "").split()

    return [
        word
        for word in words
        if len(word) >= 2 and word not in STOP_WORDS
    ]


def search_lender_chunks(
    db: Session,
    question: str,
    limit: int = 5,
) -> list[LenderChunk]:
    keywords = extract_keywords(question)

    if not keywords:
        return []

    filters = []

    for keyword in keywords:
        filters.append(LenderChunk.chunk_text.ilike(f"%{keyword}%"))
        filters.append(LenderChunk.sheet_name.ilike(f"%{keyword}%"))

    return (
        db.query(LenderChunk)
        .filter(or_(*filters))
        .limit(limit)
        .all()
    )