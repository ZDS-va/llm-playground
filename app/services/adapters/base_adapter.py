from abc import ABC, abstractmethod


class BaseAdapter(ABC):

    @abstractmethod
    def chat(
        self, model: str, messages: list[dict[str, str]], stream: bool | None = False
    ) -> dict:
        # 返回{
        #     "reply": reply,
        #     "raw": completion
        # }
        pass

    def chat_with_tools(
        self,
        model: str,
        messages: list,
        tools: list,
        tools_choice: str | None = None,
    ) -> dict:
        # 返回{
        #     "reply": reply,
        #     "raw": completion
        # }
        # 子类没有override这个方法，就抛出异常
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support tool calling."
        )
