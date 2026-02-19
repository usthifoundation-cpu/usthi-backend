from fastapi import APIRouter, Depends

from app.database import get_db
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_service import ContactService

contactRouter = APIRouter(prefix="/contacts", tags=["Contacts"])
service = ContactService()


@contactRouter.post("/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db=Depends(get_db)):
    return service.create_contact(db, contact)


@contactRouter.get("/", response_model=list[ContactResponse])
def get_contacts(db=Depends(get_db)):
    return service.get_all_contacts(db)


@contactRouter.put("/{contact_id}/read")
def mark_contact_read(contact_id: str, db=Depends(get_db)):
    return service.mark_contact_as_read(db, contact_id)


@contactRouter.delete("/{contact_id}")
def delete_contact(contact_id: str, db=Depends(get_db)):
    return service.delete_contact(db, contact_id)


@contactRouter.get("/unread-count")
def unread_contact_count(db=Depends(get_db)):
    return service.unread_count(db)
