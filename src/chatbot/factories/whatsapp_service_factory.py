from chatbot.services.evolution_service import EvolutionService
from chatbot.services.meta_service import MetaService
from chatbot.factories.db_message_client_factory import get_db_message_client
from chatbot.factories.whatsapp_client_factory import get_meta_client, get_evolution_client
from chatbot.services.whatsapp_service import WhatsappService


def get_whatsapp_service(service_name: str) -> WhatsappService:
    if service_name == "official":
        return MetaService(
            whatsapp_client=get_meta_client(),
            db_message_client=get_db_message_client()
        )
    elif service_name == "evolution":
        return EvolutionService(
            whatsapp_client=get_evolution_client(),
            db_message_client=get_db_message_client()
        )
    else:
        raise ValueError("Invalid WhatsApp service")
