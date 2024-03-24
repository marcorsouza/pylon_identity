from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from pylon_identity.api.schemas.role_schema import RolePublic, RoleSimple


class UserSchema(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str
    is_locked_out: bool


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    username: str
    is_locked_out: bool
    creation_date: datetime
    last_login_date: Optional[datetime]
    last_change: Optional[datetime]
    roles: list[RolePublic]


class UserRole(BaseModel):
    roles: list[RoleSimple]


class UserList(BaseModel):
    users: list[UserPublic]
