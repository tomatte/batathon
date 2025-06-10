from chatbot.singletons.agent_execution_control import agent_execution_control
from chatbot.tools.utils import extract_phone_number
from chatbot.models.evolution_webhook import WebhookPayload
from chatbot.clients.evolution_client import EvolutionClient


class CommandService:
    def __init__(self, evolution_client: EvolutionClient):
        self.evolution_client = evolution_client


        self.owner_commands = {
            "test_command": self._test_owner_command
        }

        self.user_commands = {
            "test_command": self._test_user_command,
        }

    async def execute_command(self, payload: WebhookPayload):
        command = payload.data.message.conversation
        self.payload = payload
        self.phone = extract_phone_number(payload)

        if payload.data.key.from_me and command in self.owner_commands:
            await self.owner_commands[command]()
        elif not payload.data.key.from_me and command in self.user_commands:
            await self.user_commands[command]()
        else:
            self._change_agent_state(command)

    async def _test_owner_command(self):
        print("Executing owner test_command")
        await self.evolution_client.send_text_message(
            self.phone,
            "The command was executed successfully",
        )

    async def _test_user_command(self):
        print("Executing user test_command")
        await self.evolution_client.send_text_message(
            self.phone,
            "The command was executed successfully",
        )

    def _change_agent_state(self, command: str):
        agent_execution_control.hello_agent(command, self.phone)
        agent_execution_control.goodbye_agent(command, self.phone)
        