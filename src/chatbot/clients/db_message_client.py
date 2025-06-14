from enum import Enum
import logging
from mcp_agent import PromptMessageMultipart
from mcp_agent.core.prompt import Prompt

logger = logging.getLogger(__name__)

class AuthorEnum(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class DBMessageClient:
    history = {}

    def add_to_history(self, user_phone: str, message: str, author: AuthorEnum):
        logger.info(f"Adding to history: {user_phone} - {message} - {author}")

        if user_phone not in self.history:
            self.history[user_phone] = []
        if author == AuthorEnum.USER:
            self.history[user_phone].append(Prompt.user(message))
        else:
            self.history[user_phone].append(Prompt.assistant(message))

    def get_history(self, user_phone: str) -> list[PromptMessageMultipart]:
        logger.info(f"Getting history: {user_phone}")  
        return self.history.get(user_phone, [])