from datetime import datetime

from pydantic import BaseModel


class ApplicationSchema(BaseModel):
    name: str
    acronym: str


class ApplicationUpdate(BaseModel):
    name: str
    acronym: str


class ApplicationPublic(BaseModel):
    id: int
    name: str
    acronym: str
    creation_date: datetime


class ApplicationList(BaseModel):
    applications: list[ApplicationPublic]


class ApplicationPagedList(BaseModel):
    data: list[ApplicationPublic]
    total_records: int
