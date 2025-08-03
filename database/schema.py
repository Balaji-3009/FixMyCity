from pydantic import BaseModel, EmailStr
from uuid import UUID


class EntryBase(BaseModel):
    uuid: UUID
    email: EmailStr

class ProfileBase(BaseModel):
    name: str
    uuid: UUID
    email: EmailStr
    pno: str
    address: str

class IssuesBase(BaseModel):
    uuid: UUID
    name: str
    image: str
    lat: float
    long: float
    description: str
    status: int = 0
