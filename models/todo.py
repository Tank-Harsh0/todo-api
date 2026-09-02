from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Priority(str,Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    URGENT ="URGENT"
    
class Todo(BaseModel):
    title: str
    desc: str
    is_completed : bool = False
    priority : Priority = Priority.MEDIUM
    created_at : datetime = Field(default_factory=datetime.now)

class Update_todo(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    is_completed : Optional[bool] = False
    priority : Optional[Priority] = Priority.MEDIUM
    created_at : datetime = Field(default_factory=datetime.now)