from enum import Enum
import json
import logging
from mcp_agent import PromptMessageMultipart
from mcp_agent.core.prompt import Prompt
from chatbot.factories.get_redis_client import get_redis_client

logger = logging.getLogger(__name__)

class AuthorEnum(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ConversationService:
    def __init__(self):
        self.redis_client = get_redis_client()

    def _save_conversation(self, user_phone: str, conversation: list[dict]):
        self.redis_client.set(f"conversation:{user_phone}", json.dumps(conversation), ex=60 * 30)

    def _get_conversation(self, user_phone: str) -> list[PromptMessageMultipart]:
        conversation = self.redis_client.get(f"conversation:{user_phone}")
        return json.loads(conversation) if conversation else []

    def add_message(self, user_phone: str, message: str, author: AuthorEnum):
        logger.info(f"Adding to history: {user_phone} - {message} - {author}")

        conversation = self._get_conversation(user_phone)

        role = "user" if author == AuthorEnum.USER else "assistant"
        conversation.append({
            "role": role,
            "content": message
        })
        
        self._save_conversation(user_phone, conversation)

    def get_messages(self, user_phone: str) -> list[PromptMessageMultipart]:
        logger.info(f"Getting history: {user_phone}")  
        return self._get_conversation(user_phone)
    
    def get_messages_multipart(self, user_phone: str) -> list[PromptMessageMultipart]:
        messages = self._get_conversation(user_phone)
        messages_multipart = []
        for message in messages:
            if message["role"] == "user":
                messages_multipart.append(Prompt.user(message["content"]))
            else:
                messages_multipart.append(Prompt.assistant(message["content"]))
        return messages_multipart
