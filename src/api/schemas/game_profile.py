from pydantic import BaseModel, Field, field_validator, ValidationError
from bson import ObjectId

class GameProfile(BaseModel):
    local_id: str
    user_id: str
    first_name: str
    last_name: str
    image_path: str
    max_click_level: int
    max_cursor_level: int


class GameProfileInDB(BaseModel):
    id: str = Field(..., example="6122a42e67a51d001555de9a")
    gameProfile: GameProfile

    @field_validator('id')
    def validate_object_id(cls, v):
        try:
            ObjectId(v)
        except Exception:
            raise ValueError('Invalid ObjectId')
        return v
    
    @classmethod
    def from_mongo(cls, data):
        return cls(id=str(data["_id"]), letter=GameProfile(content=data["content"]))

    def to_mongo(self):
        return self.model_dump()