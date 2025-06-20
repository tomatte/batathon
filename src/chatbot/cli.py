import asyncio

from importlib import import_module

from chatbot.clients.database import Database
from chatbot.factories.db_message_client_factory import get_db_message_client
from chatbot.factories.whatsapp_client_factory import get_evolution_client
from chatbot.models.whatsapp_models import Message
from chatbot.services.chatbot_service import ChatbotService
from chatbot.singletons.fast_agent_singleton import fast_agent_singleton

from chatbot.models.evolution_webhook import WebhookPayload
from chatbot.factories.evolution_service_factory import get_evolution_service
import os
import dotenv

dotenv.load_dotenv()

payload = {
    'event': 'messages.upsert',
    'instance': 'test',
    'data': {
        'key': {
            'remoteJid': '5533988902641@s.whatsapp.net', 
            'fromMe': False, 
            'id': 'F57C3A43DE15F6A2A24B9C0B257E5657'
        },
        'pushName': 'Juninho', 
        'status': 'DELIVERY_ACK', 
        'message': {
            'conversation': '', 
            'messageContextInfo': {
                'deviceListMetadata': {
                    'recipientKeyHash': '0iry88xJyWhGCw==', 
                    'recipientTimestamp': '1746899199'
                }, 
                'deviceListMetadataVersion': 2, 
                'messageSecret': '5tO2CFLI5QP0AAToQK5k1z0PjwVlXUkOwLla7zbpwcM='
            }
        }, 
        'messageType': 'conversation', 
        'messageTimestamp': 1746925015, 
        'instanceId': '0f602e5c-4882-45bf-90ed-8d0c7941f8e4', 
        'source': 'android'
    }, 
    'destination': 'https://chatbot.tomatte.dev/whatsapp/evolution/webhook', 
    'date_time': '2025-05-10T21:56:55.246Z', 
    'sender': '553388902641@s.whatsapp.net', 
    'server_url': 'https://evo-igcc4woo8os0ckwo88ww8sko.tomatte.dev', 
    'apikey': os.getenv('EVOLUTION_API_KEY')
}


async def main():
    db = Database()
    db.create_all()
    fast = fast_agent_singleton.fast
    # await get_evolution_client().send_image_message("5533988902641", visit_card, "teste")
    import_module('chatbot.ai.agents')
    async with fast.run() as agent_app:
        fast_agent_singleton.set_app(agent_app)
        chatbot_service = ChatbotService()
        webhook_payload = WebhookPayload(**payload)
        while True:
            message = input(">> ")
            if message == "exit":
                break
            webhook_payload.data.message.conversation = message
            await chatbot_service.process_message(Message.from_webhook(webhook_payload))


if __name__ == "__main__":
    asyncio.run(main())