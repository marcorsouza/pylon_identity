from pydantic import BaseModel


class CheckPermissionSchema(BaseModel):
    username: str
    tag_name: str
    acronym: str
    action_name: str
