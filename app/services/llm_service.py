from nt import system
from app.core.schema_loader import load_schema, validate_json_with_schema
from app.services.adapter_factory import get_adapter
from app.services.adapters.base_adapter import BaseAdapter
from app.services.adapters.deepseek_adapter import DeepseekAdapter
from app.services.adapters.qwen_adapter import QwenAdapter
from app.core.prompt_loader import load_prompt
import json
import logging

logger = logging.getLogger(__name__)


class LLMService:
    def chat(self, model: str, question: str):
        adapter = get_adapter(model)
        system_prompt = load_prompt("chat_default.md")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]
        result = adapter.chat(model, messages)
        return result["reply"]

    async def chat_stream(self, model: str, question: str):
        adapter = get_adapter(model)
        system_prompt = load_prompt("chat_default.md")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]
        completion = adapter.chat(model, messages, stream=True)
        for chunk in completion:
            yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"

    def summary_to_json(self, model: str, question: str):
        system_prompt = load_prompt("summary_ch.md")
        schema = load_schema("summary")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]
        adapter = get_adapter(model)

        def generate_and_validate(extra_instruction=None):
            msgs = messages.copy()
            if extra_instruction:
                msgs.append({"role": "system", "content": extra_instruction})
            raw = adapter.chat(model, msgs)["reply"]
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return {"error": "Summary is not valid JSON"}

            ok, error = validate_json_with_schema(data, schema)
            if not ok:
                return False, None, f"Schema validation error: {error}"
            return True, data, None

        success, data, err = generate_and_validate()
        logger.info(f"First time summary attempt: {success} {data} {err}")

        if success:
            return data
        logger.error(f"First time summary attempt failed: {err}")

        retry_msg = f"""
Your previous output did NOT follow the required JSON schema.
Error: {err}
Please output STRICT JSON only."""

        success, data, err = generate_and_validate(retry_msg)
        if success:
            return data
        return {"error": f"Second time summary attempt failed: {err}"}
