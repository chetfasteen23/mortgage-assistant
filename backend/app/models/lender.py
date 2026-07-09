from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String
from sqlalchemy.sql import func

from app.db.session import Base


class Lender(Base):
    __tablename__ = "lenders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    min_credit_score = Column(Integer, nullable=True)
    max_dti = Column(Numeric(5, 2), nullable=True)
    min_down_payment_percent = Column(Numeric(5, 2), nullable=True)

    supports_fha = Column(Boolean, default=False, nullable=False)
    supports_va = Column(Boolean, default=False, nullable=False)
    supports_conventional = Column(Boolean, default=True, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())