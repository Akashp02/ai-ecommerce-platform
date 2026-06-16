from pydantic import BaseModel


class OrderItemCreate(BaseModel):

    product_id: int
    quantity: int


class OrderCreate(BaseModel):

    address_id: int
    items: list[OrderItemCreate]


class OrderResponse(BaseModel):

    id: int
    total_amount: float
    order_status: str
    payment_status: str

    class Config:
        from_attributes = True