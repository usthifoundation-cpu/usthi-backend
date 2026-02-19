from datetime import datetime, timezone

from fastapi import UploadFile

from app.repositories.donate_repo import DonateRepository


class DonateService:

    def __init__(self):
        self.repo = DonateRepository()

    def create_document(
        self,
        db,
        name: str,
        phone: str,
        utr: str,
        pan: str | None,
        message: str,
        screenshot: UploadFile,
    ):
        screenshot.file.seek(0)
        file_bytes = screenshot.file.read()

        document = {
            "name": name,
            "phone": phone,
            "utr": utr,
            "screenshot": file_bytes,
            "pan": pan,
            "message": message,
            "read": False,
            "created_at": datetime.now(timezone.utc),
        }

        saved_doc = self.repo.save(db, document)

        return self._format_donation(saved_doc)

    def get_all_documents(self, db):
        docs = self.repo.find_all(db)
        return [self._format_donation(doc) for doc in docs]

    def mark_as_read(self, db, donation_id: str):
        donation = self.repo.mark_as_read(db, donation_id)
        if not donation:
            return None
        return self._format_donation(donation)

    def delete(self, db, donation_id: str):
        return self.repo.delete(db, donation_id)

    def unread_count(self, db):
        return {"count": self.repo.get_unread_count(db)}

    def _format_donation(self, doc: dict):
        created_at = doc.get("created_at")
        return {
            "id": doc["id"],
            "name": doc.get("name"),
            "phone": doc.get("phone"),
            "mobile": doc.get("phone"),
            "utr": doc.get("utr"),
            "image_url": f"/donate/{doc['id']}/image",
            "pan": doc.get("pan"),
            "message": doc.get("message"),
            "read": bool(doc.get("read", False)),
            "time": created_at.isoformat() if created_at else None,
        }
