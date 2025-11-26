from app.core.settings import settings
from app.services.adapters.base_adapter import BaseAdapter
from openai import OpenAI

class DeepseekAdapter(BaseAdapter):
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url
        )

    def chat(self,model:str, messages:list,stream: bool | None = False):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream = stream
        )
        if stream:
            return completion
        reply = completion.choices[0].message.content
        return {
            "reply":reply,
            "raw":completion
        }