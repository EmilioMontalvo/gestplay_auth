from pydantic import BaseModel
from typing import List, Dict
from .profile import Profile

class GameDataItemBase(BaseModel):
    
    completed: bool
    date_time: str
    elapsed_time: float
    level_id: str
    mistake: int
    profile_id: str
    score: int
    stars: int

class GameDataItem(GameDataItemBase):
    id: int
    class Config:
        from_attributes = True
        allow_arbitrary_types = True


class GameLevel(BaseModel):
    level_id: str
    game_data_items: List[GameDataItemBase]


class GameDataBase(BaseModel):
    profile_id: str
    game: str
    game_levels: List[GameLevel]


class GameData(GameDataBase):
    id: int    
    profile: Profile
    class Config:
        from_attributes = True




