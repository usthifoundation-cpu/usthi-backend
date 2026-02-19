import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is required in environment")

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
if not MONGO_DB_NAME:
    raise ValueError("MONGO_DB_NAME is required in environment")

_frontend_urls_raw = os.getenv("FRONTEND_URL")
if not _frontend_urls_raw:
    raise ValueError("FRONTEND_URL is required in environment")
FRONTEND_URLS = [url.strip() for url in _frontend_urls_raw.split(",") if url.strip()]
