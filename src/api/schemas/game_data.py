from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GameDataItem(BaseModel):
    completed: bool
    date_time: str
    elapsed_time: float
    level_id: str
    mistake: int
    profile_id: str
    score: int
    stars: int

class GameData(BaseModel):
    profile_id: str
    game_data: Dict[str, List[GameDataItem]]
