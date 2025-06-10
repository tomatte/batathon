from chatbot.factories.command_service_factory import get_command_service
from chatbot.services.evolution_service import EvolutionService
from chatbot.factories.db_message_client_factory import get_db_message_client
from chatbot.factories.whatsapp_client_factory import get_evolution_client


def get_evolution_service() -> EvolutionService:
    return EvolutionService(
        whatsapp_client=get_evolution_client(),
        db_message_client=get_db_message_client(),
        command_service=get_command_service(),
    )
