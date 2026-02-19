from fastapi import UploadFile

from app.repositories.onlyImage import ImageRepository


class OnlyImageService:

    def __init__(self):
        self.repo = ImageRepository()

    def upload_image(self, db, file: UploadFile):
        image = {
            "filename": file.filename,
            "content_type": file.content_type,
            "image_data": file.file.read(),
        }
        return self.repo.save(db, image)

    def get_all_images(self, db):
        return self.repo.find_all(db)

    def get_image_by_id(self, db, image_id: str):
        return self.repo.find_by_id(db, image_id)

    def delete_image(self, db, image_id: str):
        return self.repo.delete(db, image_id)
