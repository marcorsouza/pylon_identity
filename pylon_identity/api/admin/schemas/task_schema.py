from pydantic import BaseModel


class TaskSchema(BaseModel):
    name: str
    tag_name: str
    icon: str
    show_in_menu: str
    menu_title: str


class TaskUpdate(BaseModel):
    name: str
    tag_name: str
    icon: str
    show_in_menu: str
    menu_title: str


class TaskPublic(BaseModel):
    id: int
    name: str
    tag_name: str
    icon: str
    show_in_menu: str
    menu_title: str


class TaskList(BaseModel):
    tasks: list[TaskPublic]
