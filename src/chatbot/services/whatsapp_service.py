from typing import Any
from abc import ABC, abstractmethod


class WhatsappService(ABC):
    @abstractmethod
    async def process(self, body: dict[str, Any]):
        pass
