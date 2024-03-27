from typing import Optional

from pydantic import BaseModel


class ActionCreate(BaseModel):
    name: str


class ActionSchema(BaseModel):
    name: str
    task_id: Optional[int]


class ActionUpdate(BaseModel):
    name: str
    task_id: int


class ActionPublic(BaseModel):
    id: int
    name: str
    task_id: int


class ActionSimple(BaseModel):
    id: int


class ActionList(BaseModel):
    actions: list[ActionPublic]
