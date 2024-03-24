from pydantic import BaseModel


class RoleSchema(BaseModel):
    name: str
    application_id: int


class RoleUpdate(BaseModel):
    name: str
    application_id: int


class RolePublic(BaseModel):
    id: int
    name: str
    application_id: int


class RoleSimple(BaseModel):
    id: int
    application_id: int


class RoleList(BaseModel):
    roles: list[RolePublic]
