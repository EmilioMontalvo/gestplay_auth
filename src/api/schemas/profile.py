from pydantic import BaseModel
from .game_settings import GameSettings
from .user import User

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

    user: User
    game_settings: GameSettings
    class Config:
        from_attributes = True
