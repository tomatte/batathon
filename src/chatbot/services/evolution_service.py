from chatbot.singletons.agent_execution_control import agent_execution_control as agent_control
from chatbot.singletons.fast_agent_singleton import fast_agent_singleton
from chatbot.services.command_service import CommandService
from mcp_agent import PromptMessageMultipart

from chatbot.models.evolution_webhook import WebhookPayload
from chatbot.clients.db_message_client import AuthorEnum, DBMessageClient
from chatbot.clients.evolution_client import EvolutionClient
from chatbot.tools.utils import ensure_ninth_digit, extract_phone_number
class EvolutionService:
    def __init__(
        self,
        whatsapp_client: EvolutionClient,
        db_message_client: DBMessageClient,
        command_service: CommandService,
    ):
        print("Initializing WhatsApp Evolution Service")
        self.whatsapp_client = whatsapp_client
        self.db_message_client = db_message_client
        self.command_service = command_service

    async def _process_message(self, history: list[PromptMessageMultipart], agent_name: str) -> str:
            agent_app = fast_agent_singleton.app
            answer = await agent_app[agent_name].generate(history)
            return answer.last_text()

    async def _send_message(self, user_phone: str, message: str):
        phone_normalized = ensure_ninth_digit(user_phone)
        phone_plus = f"+{phone_normalized}"
        print(f"Sending message to {phone_plus}: {message}")
        res = await self.whatsapp_client.send_text_message(phone_plus, message)
        print("Response:", res)

    async def process(self, webhook_payload: WebhookPayload):
        print("Executing evolution service")
        await self.command_service.execute_command(webhook_payload)
        if webhook_payload.event != "messages.upsert" or webhook_payload.data.key.from_me:
            print("Not a message from user")
            return
        
        phone_number = extract_phone_number(webhook_payload)

        if not agent_control.can_execute(phone_number):
             print(f"No agent enabled for {phone_number}")
             return
        
        agent_name = agent_control.get_agent_name(phone_number)

        self.db_message_client.add_to_history(
            phone_number,
            webhook_payload.data.message.conversation,
            AuthorEnum.USER
        )
        
        history = self.db_message_client.get_history(phone_number)

        print("Processing message")
        answer = await self._process_message(history, agent_name)

        print("Sending message")
        await self._send_message(phone_number, answer)

        print("Adding to history")
        self.db_message_client.add_to_history(phone_number, answer, AuthorEnum.ASSISTANT)

        print(f"Answer: {answer}")