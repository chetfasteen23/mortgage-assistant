from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class LenderChunk(Base):
    __tablename__ = "lender_chunks"

    id = Column(Integer, primary_key=True, index=True)

    lender_file_id = Column(
        Integer,
        ForeignKey("lender_files.id"),
        nullable=False,
    )

    sheet_name = Column(Text, nullable=False)
    chunk_text = Column(Text, nullable=False)

    lender_file = relationship("LenderFile")