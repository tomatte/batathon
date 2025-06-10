from chatbot.factories.whatsapp_client_factory import get_evolution_client
from chatbot.services.command_service import CommandService


def get_command_service() -> CommandService:
    return CommandService(
        evolution_client=get_evolution_client()
    )

