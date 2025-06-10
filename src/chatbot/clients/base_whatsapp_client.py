from abc import ABC, abstractmethod


class BaseWhatsappClient(ABC):
    @abstractmethod
    async def send_text_message(self, to: str, message: str): ...