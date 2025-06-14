from enum import Enum
from chatbot.clients.db_message_client import AuthorEnum, DBMessageClient
from chatbot.factories.get_db import get_db
from chatbot.models.schema_requests import CreateUserRequest, UserRead
from chatbot.singletons.fast_agent_singleton import fast_agent_singleton
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Session, select
from chatbot.models.schemas import User, JobType
from sqlalchemy.orm import selectinload

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

@test_router.get("/db", response_model=list[UserRead])
async def db(db: Session = Depends(get_db)):
    statement = select(User).options(selectinload(User.willing_jobs))
    return db.exec(statement).all()

@test_router.post("/create_user", response_model=UserRead)
async def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    user = User(name=request.name, phone=request.phone)
    for job_type in request.willing_jobs:
        job_type_obj = JobType(description=job_type.description)
        user.willing_jobs.append(job_type_obj)
    db.add(user)
    db.commit()
    return user