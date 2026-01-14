import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI

from app.api.nfpa import router as nfpa_router
from app.api.cen import router as cen_router

LOG_DIR = os.path.join(os.path.dirname(__file__), "app", "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"{datetime.today():%Y%m%d}.log")

formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=2 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

app = FastAPI(title="Standards Playwright API", version="1.0.0")

app.include_router(nfpa_router)
app.include_router(cen_router)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "server_time": datetime.utcnow().isoformat() + "Z"}

@app.get("/healthabc")
def health_check() -> dict:
    return {"status": "ok", "server_time": datetime.utcnow().isoformat() + "Z"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
