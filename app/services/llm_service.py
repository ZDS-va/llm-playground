from nt import system
from app.services.adapter_factory import get_adapter
from app.services.adapters.base_adapter import BaseAdapter
from app.services.adapters.deepseek_adapter import DeepseekAdapter
from app.services.adapters.qwen_adapter import QwenAdapter
from app.core.prompt_loader import load_prompt

class LLMService:
    def chat(self,model: str,question: str):
        adapter = get_adapter(model)
        system_prompt = load_prompt("chat_default.md")
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":question}
        ]
        result = adapter.chat(model,messages)
        return result["reply"]

    async def chat_stream(self, model:str, question: str):
        adapter = get_adapter(model)
        system_prompt= load_prompt("chat_default.md")
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":question}
        ]
        completion = adapter.chat(model,messages,stream=True)
        for chunk in completion:
            yield  f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"

    def summary_to_json(self,model: str,question: str):
        system_prompt = load_prompt("summary_ch.md")
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":question}
        ]
        adapter = get_adapter(model)
        raw = adapter.chat(model,messages)["reply"]
        print(f"raw summary: {raw}")
        import json
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {"error": "Summary is not valid JSON"}
        return data
