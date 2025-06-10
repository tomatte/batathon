from chatbot.services.evolution_service import EvolutionService
from chatbot.factories.db_message_client_factory import get_db_message_client
from chatbot.factories.whatsapp_client_factory import get_meta_client, get_evolution_client


def get_evolution_service():
    return EvolutionService(
        whatsapp_client=get_evolution_client(),
        db_message_client=get_db_message_client()
    )