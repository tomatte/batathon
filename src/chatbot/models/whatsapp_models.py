from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    number: str
    text: str