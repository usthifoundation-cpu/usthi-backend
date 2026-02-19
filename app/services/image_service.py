from fastapi import UploadFile

from app.repositories.image_repo import ImageRepository


class ImageService:

    def __init__(self):
        self.repo = ImageRepository()

    def add_image(self, db, file: UploadFile, description: str, heading: str):
        image_bytes = file.file.read()

        image = {
            "filename": file.filename,
            "content_type": file.content_type,
            "description": description,
            "image_data": image_bytes,
            "heading": heading,
        }

        return self.repo.save(db, image)

    def get_all_images(self, db):
        return self.repo.get_all(db)

    def get_image(self, db, image_id: str):
        return self.repo.get_by_id(db, image_id)

    def delete_image(self, db, image_id: str):
        return self.repo.delete(db, image_id)
