from pydantic import BaseModel,BeforeValidator
from typing import List, Dict
from bson import ObjectId
from pydantic import Field
from typing import Optional
from pydantic.types import Annotated



PyObjectId = Annotated[str, BeforeValidator(str)]

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

class GameDataMongoDB(GameData):
    id:Optional[PyObjectId] = Field(alias="_id", default=None)
    game: str
    profile_id_db: int

    class Config:
        populate_by_name=True
        arbitrary_types_allowed=True
        json_schema_extra = {
            "example": {
                "game_data": {
                    "click": [
                        {
                            "completed": True,
                            "date_time": "2021-08-08T00:00:00",
                            "elapsed_time": 0.5,
                            "level_id": "1",
                            "mistake": 0,
                            "profile_id": "1",
                            "score": 100,
                            "stars": 3
                        }
                    ]
                },
                "profile_id": "1"
            }
        }


class GameDataResponse(BaseModel):
    game_data: GameData
    profile_id: str

    def dump(self):
        return {self.profile_id: self.game_data.model_dump()}



