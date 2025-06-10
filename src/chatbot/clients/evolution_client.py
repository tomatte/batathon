import httpx
from chatbot.clients.base_whatsapp_client import BaseWhatsappClient


class EvolutionClient(BaseWhatsappClient):

    def __init__(self, api_key: str, base_url: str, instance_id: str):
        self.base_url = base_url
        self.instance_id = instance_id
        self.headers = {
            "apikey": api_key,
            "Content-Type": "application/json"
        }

    async def send_text_message(self, to: str, message: str):
        url = f"{self.base_url}/message/sendText/{self.instance_id}"

        payload = {
            "number": to,
            "text": message
        }

        async with httpx.AsyncClient() as client:
            print("Sending text message from WhatsApp Evolution")
            response = await client.post(url, headers=self.headers, json=payload)
            print(f"Response: {response.text}")
