from calendar import c
from venv import logger
from .base_tool import BaseTool


class MapTool(BaseTool):
    def name(self) -> str:
        return "get_country_num"

    def description(self) -> str:
        return "根据用户输入的国家，返回在《地理手册》中的代号"

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "用户输入的国家",
                },
            },
            "required": ["country"],
        }

    def call(self, country: str) -> str:
        logger.info(f"MapTool call with country: {country}")
        if country.startswith("a"):
            return f"用户输入的国家在《地理手册》中的代号是{country}+'2'+{country}"
        else:
            return f"用户输入的国家在《地理手册》中的代号是{country}+'1'+{country}"
