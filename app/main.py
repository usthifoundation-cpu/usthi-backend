from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import FRONTEND_URLS
from app.controllers.contact_controller import contactRouter as contact_router
from app.controllers.donateController import legacy_router as legacy_donate_router, router as donate_router
from app.controllers.image_controller import Image_router as image_router
from app.controllers.login_controller import loginRouter as login_router
from app.controllers.onlyImage import OnlyImagerouter as onlyImageRouter

app = FastAPI(title="NGO Backend")

# Add root route to prevent 404 at /
@app.get("/")
def read_root():
    return {"message": "USTHI backend is running!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(contact_router)
app.include_router(donate_router)
app.include_router(legacy_donate_router)
app.include_router(login_router)
app.include_router(image_router)
app.include_router(onlyImageRouter)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
