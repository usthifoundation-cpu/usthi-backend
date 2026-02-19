from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from app.database import get_db
from app.schemas.image import ImageResponse
from app.services.image_service import ImageService

Image_router = APIRouter(prefix="/images", tags=["Images"])
service = ImageService()


@Image_router.post("/")
def upload_image(
    description: str = Form(...),
    heading: str = Form(...),
    file: UploadFile = File(...),
    db=Depends(get_db),
):
    image = service.add_image(db, file, description, heading)

    return {
        "id": image["id"],
        "filename": image["filename"],
        "description": image["description"],
        "heading": image["heading"],
        "message": "Image uploaded successfully",
    }


@Image_router.get("/", response_model=list[ImageResponse])
def get_all_images(db=Depends(get_db)):
    images = service.get_all_images(db)
    return [
        {
            "id": img["id"],
            "filename": img["filename"],
            "description": img.get("description"),
            "heading": img.get("heading"),
            "image_url": f"/images/{img['id']}",
        }
        for img in images
    ]


@Image_router.get("/{image_id}")
def get_image(image_id: str, db=Depends(get_db)):
    image = service.get_image(db, image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=image["image_data"], media_type=image["content_type"])


@Image_router.delete("/{image_id}")
def delete_image(image_id: str, db=Depends(get_db)):
    deleted = service.delete_image(db, image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted"}
