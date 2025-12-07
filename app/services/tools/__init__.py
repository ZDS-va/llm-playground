from app.services.tools.map_tool import MapTool
from .weather_tool import WeatherTool

TOOLS_LIST = {WeatherTool(), MapTool()}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": tool.name(),
            "description": tool.description(),
            "parameters": tool.parameters(),
        },
    }
    for tool in TOOLS_LIST
]

TOOLS = {tool.name(): tool for tool in TOOLS_LIST}
