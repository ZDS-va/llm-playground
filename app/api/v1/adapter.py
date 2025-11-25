from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_adapter import LLMAdapter
from app.services.llm_service import LLMService

router = APIRouter()
adaptor = LLMAdapter()
llm_service = LLMService()

class Dialogue(BaseModel):
    name: str
    question: str
    description: str | None = None


@router.get("/health")
async def health():
    return {"message":"good"}

@router.post("/dialogue")
async def diologue(dialogue: Dialogue):
    try:
        return llm_service.chat(dialogue.question)
    except Exception as e:
        return {"error":str(e)}

@router.post("/summary")
async def summary(dialogue: Dialogue):
    try:
        return llm_service.summary_to_json(dialogue.question)
    except Exception as e:
        return {"error":str(e)}
