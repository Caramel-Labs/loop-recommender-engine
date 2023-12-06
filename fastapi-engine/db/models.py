from mongoengine import connect, Document, StringField
from typing import List, Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    firstName: str
    lastName: str
    isAdmin: bool
