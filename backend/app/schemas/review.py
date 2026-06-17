from pydantic import BaseModel
from pydantic import Field


class ReviewCreate(BaseModel):

    rating: int = Field(
        ge=1,
        le=5
    )

    review_text: str


class ReviewUpdate(BaseModel):

    rating: int = Field(
        ge=1,
        le=5
    )

    review_text: str


class ReviewResponse(BaseModel):

    id: int
    product_id: int
    user_id: int
    rating: int
    review_text: str

    class Config:
        from_attributes = True