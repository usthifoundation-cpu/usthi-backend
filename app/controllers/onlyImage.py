from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response

from app.database import get_db
from app.schemas.onlyImage import ImageResponse
from app.services.onlyImage import OnlyImageService

OnlyImagerouter = APIRouter(prefix="/onlyImage", tags=["OnlyImages"])
service = OnlyImageService()


@OnlyImagerouter.post("/upload")
def upload_image(file: UploadFile = File(...), db=Depends(get_db)):
    image = service.upload_image(db, file)
    return {
        "id": image["id"],
        "message": "Image uploaded successfully",
    }


@OnlyImagerouter.get("/", response_model=list[ImageResponse])
def get_all_images(db=Depends(get_db)):
    images = service.get_all_images(db)
    return [
        ImageResponse(
            id=img["id"],
            filename=img["filename"],
            image_url=f"/onlyImage/{img['id']}",
        )
        for img in images
    ]


@OnlyImagerouter.get("/{image_id}")
def get_image(image_id: str, db=Depends(get_db)):
    image = service.get_image_by_id(db, image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=image["image_data"], media_type=image["content_type"])


@OnlyImagerouter.delete("/{image_id}")
def delete_image(image_id: str, db=Depends(get_db)):
    deleted = service.delete_image(db, image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted"}
