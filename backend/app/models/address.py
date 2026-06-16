from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Address(Base):

    __tablename__ = "addresses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    full_name = Column(
        String,
        nullable=False
    )

    phone_number = Column(
        String,
        nullable=False
    )

    address_line1 = Column(
        String,
        nullable=False
    )

    address_line2 = Column(
        String,
        nullable=True
    )

    city = Column(
        String,
        nullable=False
    )

    state = Column(
        String,
        nullable=False
    )

    country = Column(
        String,
        nullable=False
    )

    postal_code = Column(
        String,
        nullable=False
    )

    is_default = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )