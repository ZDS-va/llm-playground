from .base_tool import BaseTool


class WeatherTool(BaseTool):
    def name(self) -> str:
        return "get_weather"

    def description(self) -> str:
        return "Get the weather for a city on a specific date."

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get the weather for.",
                },
                "date": {
                    "type": "string",
                    "description": "The date to get the weather for.",
                },
            },
            "required": ["city", "date"],
        }

    def call(self, city: str, date: str) -> dict:
        return {"city": city, "date": date, "weather": "Sunny", "temperature": "25°C"}
