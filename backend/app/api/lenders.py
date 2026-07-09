from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.lender import Lender
from app.schemas.lender import LenderCreate, LenderResponse


router = APIRouter(prefix="/lenders", tags=["lenders"])


@router.post("/", response_model=LenderResponse)
def create_lender(lender_data: LenderCreate, db: Session = Depends(get_db)):
    lender = Lender(**lender_data.model_dump())

    db.add(lender)
    db.commit()
    db.refresh(lender)

    return lender


@router.get("/", response_model=list[LenderResponse])
def list_lenders(db: Session = Depends(get_db)):
    return db.query(Lender).filter(Lender.is_active == True).all()