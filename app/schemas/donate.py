from pydantic import BaseModel
from typing import Optional


class DonateSchema(BaseModel):
    id: int
    name: str
    phone: str
    utr: str
    pan: str
    message: str

    class Config:
        from_attributes  = True
