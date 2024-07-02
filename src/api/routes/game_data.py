import os
from typing import Annotated
from fastapi import Depends,APIRouter,HTTPException,status
from ..utils.auth import get_current_user,oauth2_scheme

from ..db import crud, document_crud
from ..db.database import SessionLocal, engine
from sqlalchemy.orm import Session
from ..schemas.user import User
from ..schemas.game_data import GameData, GameDataMongoDB

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    tags=["Game Data Routes"]
)

collection_name = "game_data"

# GameData routes
@router.post("/game_data", summary="Create a new game data", description="This route allows you to create a new game data.")
async def create_game_data(token: Annotated[str, Depends(oauth2_scheme)],game_data: GameData,profile_id_db,game: str, db = Depends(get_db)):
    
    if not(game=="click" or game=="cursor"):
        raise HTTPException(status_code=400,detail="Invalid game type")
    
    current_user = await get_current_user(db,token)
    profile = await profile_verify(db,profile_id_db,current_user)

    game_data_mongodb = GameDataMongoDB(**game_data.model_dump(),
                                        game = game,
                                        profile_id_db = profile.id)
    
    game_data_temp = await document_crud.create_document(collection_name,game_data_mongodb)

    if game_data_temp is None:
        raise HTTPException(status_code=500,detail="Internal server error")
    return game_data_temp



async def profile_verify(db: Session,profile_id:int,current_user: User):
    profile = crud.get_profile(db,profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    if not crud.get_profiles_of_user(db,current_user.id):
        raise HTTPException(status_code=400,detail="You don't have any profiles to share")
    
    profile_to_share=crud.get_profile_if_user_owns_profile(db,profile_id=profile_id,user_id=current_user.id)
    if not profile_to_share:
        raise HTTPException(status_code=403,detail="You don't own this profile")

    return profile