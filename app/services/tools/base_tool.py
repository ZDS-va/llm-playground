from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    工具基类，所有工具都必须继承这个类。
    """

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def parameters(self) -> dict:
        pass

    @abstractmethod
    def call(self, **kwargs) -> dict:
        pass
