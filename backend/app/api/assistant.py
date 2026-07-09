from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.llm import answer_with_context
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

    context_chunks = [chunk.chunk_text for chunk in chunks]

    answer = answer_with_context(
        question=request.question,
        context_chunks=context_chunks,
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            {
                "sheet_name": chunk.sheet_name,
                "chunk_text": chunk.chunk_text,
            }
            for chunk in chunks
        ],
    }