from typing import List, Optional

from pydantic import BaseModel

from pylon_identity.api.admin.schemas.action_schema import (
    ActionCreate,
    ActionPublic,
)


class TaskSchema(BaseModel):
    name: str
    tag_name: str
    icon: str
    show_in_menu: int
    menu_title: str
    actions: Optional[List[ActionCreate]]


class TaskUpdate(BaseModel):
    name: str
    tag_name: str
    icon: str
    show_in_menu: int
    menu_title: str
    # actions: Optional[List[ActionCreate]]


class TaskPublic(BaseModel):
    id: int
    name: str
    tag_name: str
    icon: str
    show_in_menu: int
    menu_title: str
    actions: List[ActionPublic]


class TaskList(BaseModel):
    tasks: List[TaskPublic]
