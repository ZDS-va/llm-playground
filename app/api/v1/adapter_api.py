from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import LLMService
from fastapi.responses import StreamingResponse

router = APIRouter()
llm_service = LLMService()

class Dialogue(BaseModel):
    name: str | None = None
    model: str
    question: str
    description: str | None = None


@router.get("/health")
async def health():
    return {"message":"good"}

@router.post("/dialogue")
async def diologue(dialogue: Dialogue):
    try:
        return llm_service.chat(dialogue.model,dialogue.question)
    except Exception as e:
        return {"error":str(e)}

@router.post("/dialogue_stream")
async def diologue_stream(dialogue: Dialogue):
    try:
        return StreamingResponse(llm_service.chat_stream(dialogue.model,dialogue.question),media_type="text/event-stream")
    except Exception as e:
        return {"error":str(e)}


# 临时用于浏览器/简单客户端测试的 GET SSE 接口
# 通过查询参数传递 model 与 question，便于直接用 URL 测试
@router.get("/stream_chat")
async def stream_chat(model: str = "qwen3-max", question: str = "请非常详细地介绍什么叫机器学习"):
    try:
        return StreamingResponse(llm_service.chat_stream(model, question), media_type="text/event-stream")
    except Exception as e:
        return {"error": str(e)}

@router.post("/summary")
async def summary(dialogue: Dialogue):
    try:
        return llm_service.summary_to_json(dialogue.model,dialogue.question)
    except Exception as e:
        return {"error":str(e)}
