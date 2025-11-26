from app.services.adapters.base_adapter import BaseAdapter
from app.services.adapters.deepseek_adapter import DeepseekAdapter
from app.services.adapters.qwen_adapter import QwenAdapter

def get_adapter(model:str)->BaseAdapter:
    if model.startswith("qwen"):
        return QwenAdapter()
    elif model.startswith("deepseek"):
        return DeepseekAdapter()
    else:
        raise ValueError(f"Unsupported model: {model}")