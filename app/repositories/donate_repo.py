from app.utils.mongo_utils import get_object_id, normalize_document


class DonateRepository:

    def save(self, db, document: dict):
        result = db.donation.insert_one(document)
        saved = db.donation.find_one({"_id": result.inserted_id})
        return normalize_document(saved)

    def find_all(self, db):
        docs = db.donation.find({}, {"screenshot": 0}).sort("_id", -1)
        return [normalize_document(doc) for doc in docs]

    def find_by_id(self, db, doc_id: str):
        object_id = get_object_id(doc_id)
        if object_id is None:
            return None

        doc = db.donation.find_one({"_id": object_id})
        return normalize_document(doc)

    def mark_as_read(self, db, doc_id: str):
        object_id = get_object_id(doc_id)
        if object_id is None:
            return None

        db.donation.update_one({"_id": object_id}, {"$set": {"read": True}})
        doc = db.donation.find_one({"_id": object_id}, {"screenshot": 0})
        return normalize_document(doc)

    def delete(self, db, doc_id: str):
        object_id = get_object_id(doc_id)
        if object_id is None:
            return False
        result = db.donation.delete_one({"_id": object_id})
        return result.deleted_count > 0

    def get_unread_count(self, db):
        return db.donation.count_documents(
            {"$or": [{"read": False}, {"read": {"$exists": False}}]}
        )
