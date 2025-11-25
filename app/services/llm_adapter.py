from openai import OpenAI
from app.core.settings import settings


class LLMAdapter:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.dashscope_api_key,
            base_url=settings.dashscope_base_url
        )

    def chat(self, model: str, messages: list):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages
        )

        reply = completion.choices[0].message.content
        return {
            "reply": reply,
            "raw": completion
        }

