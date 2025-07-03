import sqlite3

from sqlmodel import SQLModel,Field
from pydantic import ConfigDict
from typing import Optional


class ProfileBase(SQLModel):
    Name: str= Field(..., min_length=1,max_length=100)
    Relationship: str= Field(..., min_length=1,max_length=100)
    Message: str= Field(..., min_length=1,max_length=5000)
    image_path: str= Field(default=None)
    confirmation: bool= Field(default=False)

class ProfileSQL(ProfileBase):
    __tablename__= "profiles"
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)