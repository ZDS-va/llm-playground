from abc import ABC, abstractmethod

class BaseAdapter(ABC):

    @abstractmethod
    def chat(self,model: str, messages: list[dict[str, str]]) -> dict:
        # 返回{
        #     "reply": reply,
        #     "raw": completion
        # }
        pass