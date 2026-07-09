from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.lender_file import LenderFile
from app.models.user import User


router = APIRouter(prefix="/lender-files", tags=["lender files"])


@router.get("/current")
def get_current_lender_file(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lender_file = db.query(LenderFile).order_by(LenderFile.uploaded_at.desc()).first()

    if not lender_file:
        return {"has_file": False}

    return {
        "has_file": True,
        "id": lender_file.id,
        "filename": lender_file.filename,
        "uploaded_at": lender_file.uploaded_at,
    }