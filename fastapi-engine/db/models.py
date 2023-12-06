from mongoengine import connect, Document, StringField
from typing import List, Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    firstName: str
    username: str
    lastName: str
    interests: List[str]


class Event(BaseModel):
    name: str
    hashtags: List[str]
