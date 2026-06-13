from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from datetime import datetime

from app.db.base import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    sku = Column(
        String,
        unique=True,
        nullable=False
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        String
    )

    price = Column(
        Float,
        nullable=False
    )

    stock_quantity = Column(
        Integer,
        default=0
    )

    is_available = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )