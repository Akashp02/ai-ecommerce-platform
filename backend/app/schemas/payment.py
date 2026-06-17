from pydantic import BaseModel

from app.enums.payment_method import PaymentMethod


class PaymentCreate(BaseModel):

    payment_method: PaymentMethod


class PaymentResponse(BaseModel):

    id: int
    order_id: int
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str | None

    class Config:
        from_attributes = True