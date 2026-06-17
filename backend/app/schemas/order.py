from pydantic import BaseModel

from app.enums.order_status import OrderStatus
from app.enums.payment_status import PaymentStatus


class OrderItemCreate(BaseModel):

    product_id: int
    quantity: int


class OrderCreate(BaseModel):

    address_id: int
    items: list[OrderItemCreate]


class OrderStatusUpdate(BaseModel):

    order_status: OrderStatus


class PaymentStatusUpdate(BaseModel):

    payment_status: PaymentStatus


class OrderItemResponse(BaseModel):

    product_id: int
    quantity: int
    price_at_purchase: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):

    id: int
    total_amount: float
    order_status: str
    payment_status: str

    class Config:
        from_attributes = True


class OrderDetailResponse(BaseModel):

    id: int
    total_amount: float
    order_status: str
    payment_status: str
    items: list[OrderItemResponse]