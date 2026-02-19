from pydantic import BaseModel

class ImageResponse(BaseModel):
    id: str
    filename: str
    image_url: str

    class Config:
        from_attributes = True
