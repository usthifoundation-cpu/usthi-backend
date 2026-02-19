from pydantic import BaseModel


class ContactCreate(BaseModel):
    name: str | None = None
    fullName: str | None = None
    phone: str | None = None
    mobile: str | None = None
    email: str
    subject: str | None = None
    message: str


class ContactResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: str
    subject: str | None = None
    message: str
    read: bool = False
    time: str | None = None

    class Config:
        from_attributes = True
