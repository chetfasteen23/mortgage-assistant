from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.config import settings
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

    embedding = Column(
        Vector(settings.embedding_dimensions),
        nullable=True,
    )

    lender_file = relationship("LenderFile")