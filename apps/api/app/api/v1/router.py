from fastapi import APIRouter
from app.api.v1.routes_sources import router as sources_router

router = APIRouter(prefix="/v1")
router.include_router(sources_router, prefix="/sources", tags=["sources"])
