from pydantic import BaseModel

class ImageResponse(BaseModel):
    id: str
    filename: str
    description: str | None = None
    heading: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True
