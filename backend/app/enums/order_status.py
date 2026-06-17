
from enum import Enum


class OrderStatus(str, Enum):

    pending = "pending"
    confirmed = "confirmed"
    processing = "processing"
    shipped = "shipped"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"
    returned = "returned"