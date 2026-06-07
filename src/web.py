import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# настройка джанго орм
from orm_setup import setup_orm
setup_orm()

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from database import get_long_url
import logging

# логирование (DEBUG для отладки)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ShortShrimpLink Redirect Service")

# обработчик запросов
@app.get("/{short_code}")
async def redirect(short_code: str):
    logger.debug(f"Received request for short_code: {short_code}")
    try:
        long_url = await get_long_url(short_code)
        logger.debug(f"Found long_url: {long_url}")
        if not long_url:
            raise HTTPException(status_code=404, detail="Short link not found")
        return RedirectResponse(url=long_url)
    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail=str(e))

# проверка, что всё живое
@app.get("/")
async def root():
    return {"message": "ShortShrimpLink service is running. Use /{short_code} to redirect."}