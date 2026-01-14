import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.cen_runner import run_cen_with_handler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cen", tags=["cen"])


class CENRequest(BaseModel):
    query: Optional[str] = None


@router.post("", summary="Run CEN search")
async def cen_search(payload: CENRequest)-> dict:
    try:
        logger.info("cen request | query=%s", payload.query)
        results = await run_cen_with_handler(payload.query)
        logger.info("cen response | query=%s count=%s", payload.query, len(results))
        return {"query": payload.query or "(default)", "count": len(results), "results": results}
    except Exception as exc:
        logger.exception("CEN search failed")
        raise HTTPException(status_code=500, detail=str(exc))
