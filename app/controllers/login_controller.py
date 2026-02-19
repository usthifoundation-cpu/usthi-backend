from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.schemas.login import LoginRequest
from app.services.loginService import LoginService

loginRouter = APIRouter(prefix="/login", tags=["Login"])
service = LoginService()


@loginRouter.post("/")
def login(request: LoginRequest, db=Depends(get_db)):
    result = service.login(db, request.username, request.password)

    if result["status"] == 403:
        raise HTTPException(status_code=403, detail=result["message"])

    return {
        "status": "success",
        "message": result["message"],
    }
