from pydantic import BaseModel


class CategoryCreate(BaseModel):

    name: str
    description: str


class CategoryResponse(BaseModel):

    id: int
    name: str
    slug: str
    description: str

    class Config:

        from_attributes = True