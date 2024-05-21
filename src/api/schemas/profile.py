from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True
