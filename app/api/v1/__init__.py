from fastapi import APIRouter
from . import adapter_api

router = APIRouter()

router.include_router(adapter_api.router, prefix="/llm",tags=["diologue"])