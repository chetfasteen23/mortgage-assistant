from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.retrieval import search_lender_chunks


router = APIRouter(prefix="/assistant", tags=["assistant"])


class AssistantQuestion(BaseModel):
    question: str


@router.post("/ask")
def ask_assistant(
    request: AssistantQuestion,
    db: Session = Depends(get_db),
):
    chunks = search_lender_chunks(
        db=db,
        question=request.question,
        limit=5,
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