from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.session import Base


class LenderFile(Base):
    __tablename__ = "lender_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())