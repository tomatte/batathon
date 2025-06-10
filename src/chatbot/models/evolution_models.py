from pydantic import BaseModel


class EvolutionSendText(BaseModel):
    number: str
    message: str
