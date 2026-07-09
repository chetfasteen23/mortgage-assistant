from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class LenderGuideline(Base):
    __tablename__ = "lender_guidelines"

    id = Column(Integer, primary_key=True, index=True)

    lender_file_id = Column(Integer, ForeignKey("lender_files.id"), nullable=False)

    sheet_name = Column(String, nullable=False)
    row_number = Column(Integer, nullable=False)

    column_name = Column(String, nullable=False)
    cell_value = Column(Text, nullable=True)

    lender_file = relationship("LenderFile")