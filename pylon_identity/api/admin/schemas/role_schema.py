from pydantic import BaseModel

from pylon_identity.api.admin.schemas.application_schema import (
    ApplicationPublic,
)


class RoleSchema(BaseModel):
    name: str
    application_id: int


class RoleUpdate(BaseModel):
    name: str
    application_id: int


class RolePublic(BaseModel):
    id: int
    name: str
    application: ApplicationPublic


class RoleSimple(BaseModel):
    id: int


class RoleList(BaseModel):
    roles: list[RolePublic]
