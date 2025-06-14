from enum import Enum
from chatbot.clients.db_message_client import AuthorEnum, DBMessageClient
from chatbot.factories.get_db import get_db
from chatbot.singletons.fast_agent_singleton import fast_agent_singleton
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

test_router = APIRouter(
    prefix="/test",
    tags=["Test"]
)

class AgentEnum(str, Enum):
    ROUTER = "jaiminho"

class Payload(BaseModel):
    prompt: str = Field(..., example="oi")
    agent: AgentEnum = AgentEnum.ROUTER
    
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

from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base, Session

from sqlalchemy import Column, Integer, String

Base = declarative_base()

from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  # This enables ORM mode

@test_router.get("/db")
async def db(db: Session = Depends(get_db)) -> list[UserResponse]:
    return db.query(User).all()