from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.lender_chunk import LenderChunk


router = APIRouter(prefix="/assistant", tags=["assistant"])


class AssistantQuestion(BaseModel):
    question: str


@router.post("/ask")
def ask_assistant(
    request: AssistantQuestion,
    db: Session = Depends(get_db),
):
    query = request.question

    chunks = (
        db.query(LenderChunk)
        .filter(
            or_(
                LenderChunk.chunk_text.ilike(f"%{query}%"),
                LenderChunk.sheet_name.ilike(f"%{query}%"),
            )
        )
        .limit(5)
        .all()
    )

    context = [
        {
            "sheet_name": chunk.sheet_name,
            "chunk_text": chunk.chunk_text,
        }
        for chunk in chunks
    ]

    return {
        "question": request.question,
        "matched_chunks": context,
        "message": "These are the lender data chunks that would be sent to the LLM.",
    }