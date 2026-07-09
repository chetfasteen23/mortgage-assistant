from pathlib import Path

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.lender_chunk import LenderChunk
from app.models.lender_file import LenderFile


router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def dataframe_to_chunks(sheet_name: str, dataframe: pd.DataFrame) -> list[str]:
    chunks = []

    dataframe = dataframe.fillna("")

    for index, row in dataframe.iterrows():
        row_parts = []

        for column_name, value in row.items():
            if str(value).strip():
                row_parts.append(f"{column_name}: {value}")

        if row_parts:
            chunk_text = f"Sheet: {sheet_name}\nRow: {index + 2}\n" + "\n".join(row_parts)
            chunks.append(chunk_text)

    return chunks


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

    db.query(LenderChunk).delete()
    db.query(LenderFile).delete()
    db.commit()

    lender_file = LenderFile(
        filename=file.filename,
        file_path=str(file_path),
    )

    db.add(lender_file)
    db.commit()
    db.refresh(lender_file)

    total_chunks = 0
    sheet_summaries = []

    for sheet_name, dataframe in excel_data.items():
        chunks = dataframe_to_chunks(sheet_name, dataframe)

        for chunk_text in chunks:
            lender_chunk = LenderChunk(
                lender_file_id=lender_file.id,
                sheet_name=sheet_name,
                chunk_text=chunk_text,
            )
            db.add(lender_chunk)

        total_chunks += len(chunks)

        sheet_summaries.append(
            {
                "sheet_name": sheet_name,
                "rows": len(dataframe),
                "chunks_created": len(chunks),
                "columns": list(dataframe.columns),
            }
        )

    db.commit()

    return {
        "file_id": lender_file.id,
        "filename": file.filename,
        "total_chunks_created": total_chunks,
        "sheets": sheet_summaries,
    }