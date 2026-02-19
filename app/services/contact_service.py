from datetime import datetime, timezone

from fastapi import HTTPException

from app.repositories.contact_repo import ContactRepository


class ContactService:

    def __init__(self):
        self.repo = ContactRepository()

    def create_contact(self, db, data):
        payload = data.model_dump()

        name = payload.get("name") or payload.get("fullName")
        phone = payload.get("phone") or payload.get("mobile")

        if not name or not phone:
            raise HTTPException(status_code=422, detail="name/phone are required")

        contact = {
            "name": name,
            "phone": phone,
            "email": payload["email"],
            "subject": payload.get("subject"),
            "message": payload["message"],
            "read": False,
            "created_at": datetime.now(timezone.utc),
        }
        return self._format_contact(self.repo.save(db, contact))

    def get_all_contacts(self, db):
        return [self._format_contact(item) for item in self.repo.find_all(db)]

    def mark_contact_as_read(self, db, contact_id: str):
        contact = self.repo.mark_as_read(db, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return self._format_contact(contact)

    def delete_contact(self, db, contact_id: str):
        deleted = self.repo.delete(db, contact_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Contact not found")
        return {"message": "Contact deleted"}

    def unread_count(self, db):
        return {"count": self.repo.get_unread_count(db)}

    def _format_contact(self, contact: dict):
        created_at = contact.get("created_at")
        return {
            "id": contact["id"],
            "name": contact.get("name"),
            "phone": contact.get("phone"),
            "email": contact.get("email"),
            "subject": contact.get("subject"),
            "message": contact.get("message"),
            "read": bool(contact.get("read", False)),
            "time": created_at.isoformat() if created_at else None,
        }
