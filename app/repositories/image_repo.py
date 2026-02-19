from app.utils.mongo_utils import get_object_id, normalize_document


class ImageRepository:

    def save(self, db, image: dict):
        result = db.images.insert_one(image)
        saved = db.images.find_one({"_id": result.inserted_id})
        return normalize_document(saved)

    def get_all(self, db):
        docs = db.images.find({}, {"image_data": 0}).sort("_id", -1)
        return [normalize_document(doc) for doc in docs]

    def get_by_id(self, db, image_id: str):
        object_id = get_object_id(image_id)
        if object_id is None:
            return None

        doc = db.images.find_one({"_id": object_id})
        return normalize_document(doc)

    def delete(self, db, image_id: str):
        object_id = get_object_id(image_id)
        if object_id is None:
            return False
        result = db.images.delete_one({"_id": object_id})
        return result.deleted_count > 0
