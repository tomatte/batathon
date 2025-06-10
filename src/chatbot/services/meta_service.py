from typing import Any, Dict, Optional

from chatbot.services.whatsapp_service import WhatsappService
from chatbot.clients.db_message_client import DBMessageClient
from chatbot.clients.meta_client import MetaClient
from chatbot.models.whatsapp_models import UserInfo
from chatbot.tools.utils import ensure_ninth_digit
from chatbot.ai.agents import fast

class MetaService(WhatsappService):
    def __init__(self, whatsapp_client: MetaClient, db_message_client: DBMessageClient):
        print("Initializing WhatsApp Official Service")
        self.whatsapp_client = whatsapp_client
        self.db_message_client = db_message_client

    def _extract_whatsapp_info(self, data: Dict[str, Any]) -> Optional[UserInfo]:
        try:
            entry = data["entry"][0]
            change = entry["changes"][0]
            value = change["value"]
            contact = value["contacts"][0]
            message = value["messages"][0]

            name = contact["profile"]["name"]
            number = contact["wa_id"]
            text = message["text"]["body"]

            return UserInfo(name=name, number=number, text=text)
        except (KeyError, IndexError, TypeError):
            return None
        
    async def _process_message(self, history: list[dict[str, str]]) -> str:
        async with fast.run() as agent:
            history_str = "\n".join([f"{item['author']}: {item['message']}" for item in history])
            answer = await agent.pedro(history_str)
            return answer

    async def _send_message(self, user_phone: str, message: str):
        phone_normalized = ensure_ninth_digit(user_phone)
        phone_plus = f"+{phone_normalized}"
        print(f"Sending message to {phone_plus}: {message}")
        res = await self.whatsapp_client.send_text_message(to=phone_plus, message=message)
        print("Response:", res)

    async def process(self, body: Dict[str, Any]):
        user_info = self._extract_whatsapp_info(body)
        if not user_info:
            print("No user info found")
            return
        self.db_message_client.add_to_history(user_info.number, user_info.text, user_info.name)
        print(f"User info: {user_info.name} - {user_info.number} - {user_info.text}")
        history = self.db_message_client.get_history(user_info.number)
        answer = await self._process_message(history)
        await self._send_message(user_info.number, answer)
        self.db_message_client.add_to_history(user_info.number, answer, "you")
        print(f"Answer: {answer}")
