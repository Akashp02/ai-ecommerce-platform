from pydantic import BaseModel


class AddressCreate(BaseModel):

    full_name: str
    phone_number: str
    address_line1: str
    address_line2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str
    is_default: bool


class AddressUpdate(BaseModel):

    full_name: str
    phone_number: str
    address_line1: str
    address_line2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str
    is_default: bool


class AddressResponse(BaseModel):

    id: int
    full_name: str
    phone_number: str
    address_line1: str
    address_line2: str | None
    city: str
    state: str
    country: str
    postal_code: str
    is_default: bool

    class Config:
        from_attributes = True