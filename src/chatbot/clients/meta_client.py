import httpx
from chatbot.clients.base_whatsapp_client import BaseWhatsappClient


class MetaClient(BaseWhatsappClient):
    def __init__(self, access_token: str, phone_number_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.api_url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    async def send_text_message(self, to: str, message: str):
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "body": message
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()