from pydantic import BaseModel, Field


class ProductCreate(BaseModel):

    sku: str
    name: str
    description: str
    price: float = Field(
        gt=0
    )
    stock_quantity: int = Field(
        ge=0
    )

class ProductUpdate(BaseModel):

    sku: str
    name: str
    description: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)

class ProductResponse(BaseModel):

    id: int
    sku: str
    name: str
    description: str
    price: float
    stock_quantity: int
    is_available: bool

    class Config:

        from_attributes = True