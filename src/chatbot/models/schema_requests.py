from pydantic import BaseModel
from sqlmodel import SQLModel


class JobTypeRead(SQLModel):
    description: str

class UserRead(SQLModel):
    name: str
    phone: str
    willing_jobs: list[JobTypeRead] = []

class CreateUserRequest(BaseModel):
    name: str
    phone: str
    willing_jobs: list[JobTypeRead]
