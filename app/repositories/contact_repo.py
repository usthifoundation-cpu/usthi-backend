from app.utils.mongo_utils import get_object_id, normalize_document


class ContactRepository:

    def save(self, db, contact: dict):
        result = db.contact.insert_one(contact)
        saved = db.contact.find_one({"_id": result.inserted_id})
        return normalize_document(saved)

    def find_all(self, db):
        docs = db.contact.find().sort("_id", -1)
        return [normalize_document(doc) for doc in docs]

    def mark_as_read(self, db, contact_id: str):
        object_id = get_object_id(contact_id)
        if object_id is None:
            return None

        db.contact.update_one({"_id": object_id}, {"$set": {"read": True}})
        doc = db.contact.find_one({"_id": object_id})
        return normalize_document(doc)

    def delete(self, db, contact_id: str):
        object_id = get_object_id(contact_id)
        if object_id is None:
            return False
        result = db.contact.delete_one({"_id": object_id})
        return result.deleted_count > 0

    def get_unread_count(self, db):
        return db.contact.count_documents(
            {"$or": [{"read": False}, {"read": {"$exists": False}}]}
        )
