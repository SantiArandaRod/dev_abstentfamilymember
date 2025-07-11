
from sqlmodel import SQLModel,Field
from pydantic import ConfigDict
from typing import Optional


class ProfileBase(SQLModel):
    Name: str= Field(..., min_length=1,max_length=100)
    Relationship: str= Field(..., min_length=1,max_length=100)
    Message: str= Field(..., min_length=1,max_length=5000)
    image_path: Optional[str] = None
    confirmation: bool= Field(default=False)

class ProfileSQL(ProfileBase, table=True):
    __tablename__ = "profiles"
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)

class ProfileUpdate(SQLModel):
    Name: Optional[str] = None
    Relationship: Optional[str] = None
    Message: Optional[str] = None
    Image_path: Optional[str] = None
    Confirmation: Optional[bool] = None