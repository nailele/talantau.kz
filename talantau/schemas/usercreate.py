from enum import Enum

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, field_validator



class UserRole(str, Enum):
    student = "student"
    employer = "employer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator('password', mode='after')
    @classmethod
    def hash_password(cls, password: str) -> str:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)
