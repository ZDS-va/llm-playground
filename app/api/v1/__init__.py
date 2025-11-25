from fastapi import APIRouter
from . import adapter

router = APIRouter()

router.include_router(adapter.router, prefix="/diologue",tags=["diologue"])