from pathlib import Path
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.lender_file import LenderFile

import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException


router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = Path("app/uploads")


@router.post("/lender-sheet")

async def upload_lender_sheet(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

):

    if not file.filename.endswith((".xlsx", ".xls")):

        raise HTTPException(status_code=400, detail="File must be an Excel file")

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:

        f.write(contents)

    try:

        excel_data = pd.read_excel(file_path, sheet_name=None)

    except Exception:

        raise HTTPException(status_code=400, detail="Could not read Excel file")

    lender_file = LenderFile(

        filename=file.filename,

        file_path=str(file_path),

    )

    db.add(lender_file)

    db.commit()

    db.refresh(lender_file)

    sheet_summaries = []

    for sheet_name, dataframe in excel_data.items():

        sheet_summaries.append(

            {

                "sheet_name": sheet_name,

                "rows": len(dataframe),

                "columns": list(dataframe.columns),

            }

        )

    return {
        "file_id": lender_file.id,
        "filename": file.filename,
        "sheets": sheet_summaries,
    }