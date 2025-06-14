from chatbot.clients.db_message_client import DBMessageClient
from chatbot.models.whatsapp_models import Message


class ChatbotService:
    def __init__(self, db_message_client: DBMessageClient):
        self.db_message_client = db_message_client

    def process_message(self, message: Message) -> str:
        print(message)
        return ""