from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):

    category_id: int
    sku: str
    name: str
    description: Optional[str] = None
    price: float = Field(
        gt=0
    )
    stock_quantity: int = Field(
        ge=0
    )

class ProductUpdate(BaseModel):

    name: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)

class ProductResponse(BaseModel):

    id: int
    category_id: int
    sku: str
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    is_available: bool

    class Config:

        from_attributes = True