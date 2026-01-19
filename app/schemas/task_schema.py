from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class TaskBase(BaseModel):
    title:str
    description:Optional[str]=None
    priority:str="medium"
    due_date:Optional[date]= None

class TaskCreate(TaskBase):
    assigned_to_id: int


class TaskUpdate(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None
    priority:Optional[str]=None
    dur_date:Optional[date]=None

class TaskResponse(TaskBase):
    id:int
    status:str
    assigned_to_id:int
    created_by_id:int
    created_at:datetime
    
    class Config:
        from_attributes = True