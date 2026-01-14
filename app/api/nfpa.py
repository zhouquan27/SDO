import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.nfpa_runner import run_nfpa_with_handler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nfpa", tags=["nfpa"])


class NFPARequest(BaseModel):
    query: Optional[str] = None


@router.post("", summary="Run NFPA search")
async def nfpa_search(payload: NFPARequest)-> dict:
    try:
        logger.info("nfpa request | query=%s", payload.query)
        results = await run_nfpa_with_handler(payload.query)
        logger.info("nfpa response | query=%s count=%s", payload.query, len(results))
        return {"query": payload.query or "(default)", "count": len(results), "results": results}
    except Exception as exc:
        logger.exception("NFPA search failed")
        raise HTTPException(status_code=500, detail=str(exc))
