import os
from chatbot.clients.base_whatsapp_client import BaseWhatsappClient
import dotenv
from chatbot.clients.evolution_client import EvolutionClient
from chatbot.clients.meta_client import MetaClient

dotenv.load_dotenv()

def get_meta_client() -> MetaClient:
    return MetaClient(
            access_token=os.getenv("META_ACCESS_TOKEN"),
            phone_number_id=os.getenv("META_PHONE_NUMBER_ID")
        )

def get_evolution_client() -> EvolutionClient:
    return EvolutionClient(
        api_key=os.getenv("EVOLUTION_API_KEY"), 
        base_url=os.getenv("EVOLUTION_BASE_URL"), 
        instance_id=os.getenv("EVOLUTION_INSTANCE_ID")
    )

_clients = {
    "meta": get_meta_client,
    "evolution": get_evolution_client,
}

def get_whatsapp_client() -> BaseWhatsappClient:
    return _clients[os.getenv("WHATSAPP_SERVICE")]()