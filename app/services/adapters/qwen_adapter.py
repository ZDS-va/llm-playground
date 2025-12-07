from openai import OpenAI
from app.core.settings import settings
from app.services.adapters.base_adapter import BaseAdapter


class QwenAdapter(BaseAdapter):
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.dashscope_api_key, base_url=settings.dashscope_base_url
        )

    def chat(self, model: str, messages: list, stream: bool | None = False):
        completion = self.client.chat.completions.create(
            model=model, messages=messages, stream=stream
        )
        if stream:
            return completion
        reply = completion.choices[0].message.content
        return {"reply": reply, "raw": completion}

    def chat_with_tools(
        self, model: str, messages: list, tools: list, tools_choice: str = "auto"
    ) -> dict:
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tools_choice,
        )
        return completion
