from typing import Type
from pydantic import BaseModel, Field


class User(BaseModel):
    email: str
    password: str
    company: str

    @classmethod
    def add_field(cls, field_name: str, field_type: Type, description: str):
        if not hasattr(cls, field_name):
            setattr(
                cls, field_name, Field(None, description=description, type=field_type)
            )
