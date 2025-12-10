from app.core.schema_loader import load_schema, validate_json_with_schema
from app.services.adapter_factory import get_adapter
from app.core.prompt_loader import load_prompt
import json
import logging

from app.services.tools import TOOLS, TOOLS_SCHEMA

logger = logging.getLogger(__name__)


class LLMService:
    def chat(self, model: str, question: str):
        adapter = get_adapter(model)
        prompt_info = load_prompt("chat_default")
        messages = [
            {"role": prompt_info["role"], "name": prompt_info["name"], "content": prompt_info["content"]},
            {"role": "user", "content": question},
        ]
        result = adapter.chat(model, messages)
        return result["reply"]

    async def chat_stream(self, model: str, question: str):
        adapter = get_adapter(model)
        prompt_info = load_prompt("chat_default")
        messages = [
            {"role": prompt_info["role"], "name": prompt_info["name"], "content": prompt_info["content"]},
            {"role": "user", "content": question},
        ]
        completion = adapter.chat(model, messages, stream=True)
        for chunk in completion:
            yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"

    def summary_to_json(self, model: str, question: str):
        prompt_info = load_prompt("summary_ch")
        schema = load_schema("summary")
        messages = [
            {"role": prompt_info["role"], "name": prompt_info["name"], "content": prompt_info["content"]},
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

    def chat_with_tools(self, model: str, question: str):
        prompt_info = load_prompt("tools")

        messages = [
            {"role": prompt_info["role"], "name": prompt_info["name"], "content": prompt_info["content"]},
            {"role": "user", "content": question},
        ]

        adapter = get_adapter(model)

        completion = adapter.chat_with_tools(model, messages, TOOLS_SCHEMA, "auto")

        choice = completion.choices[0]
        finish_reason = choice.finish_reason
        assistant_msg = choice.message

        logger.info(f"First time assistant message: {assistant_msg}")
        if finish_reason == "stop" and assistant_msg.content:
            return assistant_msg.content

        if finish_reason == "tool_calls":
            tool_call = assistant_msg.tool_calls[0]
            func_name = tool_call.function.name

            try:
                args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                return {"error": "Tool arguments are not valid JSON"}

            tool = TOOLS.get(func_name)
            logger.info(f"Tool {func_name} found: {tool}")
            if not tool:
                return {"error": f"Tool {func_name} not found"}

            tool_result = tool.call(**args)

            messages.append(
                {"role": "assistant", "content": None, "tool_calls": [tool_call]}
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result),
                }
            )

            final_completion = adapter.chat_with_tools(
                model, messages, TOOLS_SCHEMA, "none"
            )
            final_msg = final_completion.choices[0].message
            return final_msg.content or "工具调用完成，但模型无文本回答"
        return f"Unexcepted finish_reason: {finish_reason}"
