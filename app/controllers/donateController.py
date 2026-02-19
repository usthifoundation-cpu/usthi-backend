from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from app.database import get_db
from app.services.donate_service import DonateService

router = APIRouter(prefix="/donate", tags=["Donate"])
legacy_router = APIRouter(tags=["Donate"])
service = DonateService()


def _create_donation(
    db,
    name: str,
    phone: str,
    utr: str,
    pan: str | None,
    message: str,
    screenshot: UploadFile,
):
    return service.create_document(db, name, phone, utr, pan, message, screenshot)


@router.post("/")
def create_donation(
    name: str = Form(...),
    phone: str = Form(...),
    utr: str = Form(...),
    pan: str | None = Form(None),
    message: str = Form(...),
    screenshot: UploadFile = File(...),
    db=Depends(get_db),
):
    return _create_donation(db, name, phone, utr, pan, message, screenshot)


@legacy_router.post("/donation")
def create_donation_legacy(
    name: str = Form(...),
    phone: str = Form(...),
    utr: str = Form(...),
    pan: str | None = Form(None),
    message: str = Form(...),
    screenshot: UploadFile = File(...),
    db=Depends(get_db),
):
    return _create_donation(db, name, phone, utr, pan, message, screenshot)


@router.get("/")
def get_all(db=Depends(get_db)):
    return service.get_all_documents(db)


@router.get("/{id}/image")
def get_donation_image(id: str, db=Depends(get_db)):
    document = service.repo.find_by_id(db, id)
    if not document or not document.get("screenshot"):
        raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=document["screenshot"], media_type="image/png")


@router.put("/{id}/read")
def mark_donation_read(id: str, db=Depends(get_db)):
    donation = service.mark_as_read(db, id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation


@router.put("/delete/{id}/read")
def mark_donation_read_legacy(id: str, db=Depends(get_db)):
    donation = service.mark_as_read(db, id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation


@router.delete("/delete/{id}")
def delete_donation(id: str, db=Depends(get_db)):
    deleted = service.delete(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Donation not found")
    return {"message": "Donation deleted"}


@router.get("/unread-count")
def donation_unread_count(db=Depends(get_db)):
    return service.unread_count(db)
