from pydantic import BaseModel

class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    image_path: str
    max_click_level: int
    max_cursor_level: int

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True
