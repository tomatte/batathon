from enum import Enum
from chatbot.clients.db_message_client import AuthorEnum, DBMessageClient
from chatbot.singletons.fast_agent_singleton import fast_agent_singleton
from fastapi import APIRouter
from pydantic import BaseModel, Field

test_router = APIRouter(
    prefix="/test",
    tags=["Test"]
)

class AgentEnum(str, Enum):
    ROUTER = "jaiminho"

class Payload(BaseModel):
    prompt: str = Field(..., example="oi pedro")
    agent: AgentEnum = AgentEnum.PEDRO
    
_db_message_client = DBMessageClient()
test_phone = "11988902640"

@test_router.post("/chat")
async def chat(payload: Payload):
    _db_message_client.add_to_history(
        test_phone,
        payload.prompt,
        AuthorEnum.USER
    )
    history = _db_message_client.get_history(test_phone)
    agent_app = fast_agent_singleton.app
    answer = await agent_app[payload.agent].generate(history)
    _db_message_client.add_to_history(test_phone, answer, AuthorEnum.ASSISTANT)
    return answer.last_text()
