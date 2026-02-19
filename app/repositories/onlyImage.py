from app.utils.mongo_utils import get_object_id, normalize_document


class ImageRepository:

    def save(self, db, image: dict):
        result = db.onlyImages.insert_one(image)
        saved = db.onlyImages.find_one({"_id": result.inserted_id})
        return normalize_document(saved)

    def find_all(self, db):
        docs = db.onlyImages.find({}, {"image_data": 0}).sort("_id", -1)
        return [normalize_document(doc) for doc in docs]

    def find_by_id(self, db, image_id: str):
        object_id = get_object_id(image_id)
        if object_id is None:
            return None

        doc = db.onlyImages.find_one({"_id": object_id})
        return normalize_document(doc)

    def delete(self, db, image_id: str):
        object_id = get_object_id(image_id)
        if object_id is None:
            return False
        result = db.onlyImages.delete_one({"_id": object_id})
        return result.deleted_count > 0
