from pydantic import BaseModel, EmailStr
from typing import List

class Email(BaseModel):
    email: List[EmailStr]


