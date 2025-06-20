from pydantic import BaseModel

class CommandRequest(BaseModel):
    command: str
