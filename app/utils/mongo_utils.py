from bson.errors import InvalidId
from bson.objectid import ObjectId


def get_object_id(value: str):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


def normalize_document(document: dict | None):
    if not document:
        return None

    normalized = dict(document)
    normalized["id"] = str(normalized.pop("_id"))
    return normalized
