from datetime import datetime

from pydantic import BaseModel, Field


class SMSSchema(BaseModel):
    number: str
    code: str
    timestamp: datetime = Field(default_factory=datetime.now)