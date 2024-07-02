from pydantic import BaseModel
from typing import List, Dict

class GameDataEntry(BaseModel):
    completed: bool
    date_time: str
    elapsed_time: float
    level_id: str
    mistake: int
    profile_id: str
    score: float
    stars: float

class GameData(BaseModel):
    game_data: Dict[str, List[GameDataEntry]]
    profile_id: str




