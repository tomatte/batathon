from chatbot.clients.db_message_client import AuthorEnum, DBMessageClient
from chatbot.models.whatsapp_models import Message
from chatbot.services.conversation_service import ConversationService
from chatbot.singletons.fast_agent_singleton import fast_agent_singleton
# get user state
# if not exists
#   verify if user exists in db
#   if not
#     set user state to "create_user"
#   if exists
#     get user
#     set user state as "discover_intent"
#     
#     once the intent is clarified, set user state to the specific intent

class ChatbotService:
    def __init__(self):
        self.conversation_service = ConversationService()
        self.fast_agent = fast_agent_singleton.app

    async def process_message(self, message: Message, agent_name: str = "jaiminho") -> str:
        self.conversation_service.add_message(message.phone, message.message, AuthorEnum.USER)
        conversation = self.conversation_service.get_messages_multipart(message.phone)
        answer = await self.fast_agent[agent_name].generate(conversation)
        last_text = answer.last_text()
        self.conversation_service.add_message(message.phone, last_text, AuthorEnum.ASSISTANT)
        return await self.fast_agent["corrige_mensagem_para_o_usuário"](last_text)
