from chatbot.models.evolution_webhook import WebhookPayload
from chatbot.tools.utils import extract_phone_number
from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    number: str
    text: str

class Message(BaseModel):
    phone: str
    message: str | None = None
    sender: str | None = None
    is_from_me: bool | None = None

    @classmethod
    def from_webhook(cls, webhook_payload: WebhookPayload) -> "Message":
        return cls(
            phone=extract_phone_number(webhook_payload),
            message=webhook_payload.data.message.conversation,
            sender=webhook_payload.data.push_name,
            is_from_me=webhook_payload.data.key.from_me
        )
