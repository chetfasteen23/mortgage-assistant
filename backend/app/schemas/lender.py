from decimal import Decimal
from pydantic import BaseModel


class LenderCreate(BaseModel):
    name: str
    min_credit_score: int | None = None
    max_dti: Decimal | None = None
    min_down_payment_percent: Decimal | None = None
    supports_fha: bool = False
    supports_va: bool = False
    supports_conventional: bool = True


class LenderResponse(LenderCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True