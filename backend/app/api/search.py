from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.lender_chunk import LenderChunk


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/lender-chunks")
def search_lender_chunks(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    results = (
        db.query(LenderChunk)
        .filter(
            or_(
                LenderChunk.chunk_text.ilike(f"%{q}%"),
                LenderChunk.sheet_name.ilike(f"%{q}%"),
            )
        )
        .limit(10)
        .all()
    )

    return [
        {
            "id": chunk.id,
            "sheet_name": chunk.sheet_name,
            "chunk_text": chunk.chunk_text,
        }
        for chunk in results
    ]