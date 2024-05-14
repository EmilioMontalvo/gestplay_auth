from pydantic import BaseModel, ConfigDict
from profile import Profile


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    profiles: list[Profile]
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed=True
        


    