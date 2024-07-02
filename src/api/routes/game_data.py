import os
from typing import Annotated
from fastapi import Depends,APIRouter,HTTPException,status
from ..utils.auth import get_current_user,oauth2_scheme

from ..db import crud
from ..db.database import SessionLocal, engine

from ..schemas.game_data import GameData

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    tags=["Game Data Routes"]
)

# GameData routes
@router.post("/game_data", summary="Create a new game data", description="This route allows you to create a new game data.")
async def create_game_data(token: Annotated[str, Depends(oauth2_scheme)],game_data: GameData,profile_id_db,game: str, db = Depends(get_db)):
    return {"message": "The game data was created successfully."}