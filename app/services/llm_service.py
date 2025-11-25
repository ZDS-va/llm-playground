from app.services.llm_adapter import LLMAdapter
from app.core.prompt_loader import load_prompt

class LLMService:
    def __init__(self,adapter: LLMAdapter | None = None):
        self.adaptor = adapter or LLMAdapter()

    def chat(self,question: str):
        system_prompt = load_prompt("chat_default.md")
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":question}
        ]
        result = self.adaptor.chat("qwen3-max",messages)
        return result["reply"]

    def summary_to_json(self,question: str):
        system_prompt = load_prompt("summary_ch.md")
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":question}
        ]
        raw = self.adaptor.chat("qwen3-max",messages)["reply"]
        print(f"raw summary: {raw}")
        import json
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {"error": "Summary is not valid JSON"}
        return data
