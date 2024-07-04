import os
from typing import Annotated
from fastapi import Depends,APIRouter,HTTPException,status
from ..utils.auth import get_current_user,oauth2_scheme
import pymongo
from ..db import crud, document_crud
from ..db.database import SessionLocal, engine
from sqlalchemy.orm import Session
from ..schemas.user import User
from ..schemas.game_data import GameData, GameDataMongoDB

def get_db_sql():
    db_sql = SessionLocal()
    try:
        yield db_sql
    finally:
        db_sql.close()

router = APIRouter(
    tags=["Game Data Routes"]
)

collection_name = "game_data"

# GameData routes
@router.post("/profiles/{profile_id_db}/game-data/{game}", summary="Create a new game data", description="This route allows you to create a new game data.")
async def create_game_data(token: Annotated[str, Depends(oauth2_scheme)],game_data: GameData,profile_id_db,game: str, db = Depends(get_db_sql)):
    
    if not(game=="click" or game=="cursor"):
        raise HTTPException(status_code=400,detail="Invalid game type")
    
    current_user = await get_current_user(db,token)
    profile = await profile_verify(db,profile_id_db,current_user)

    #verify if a collection with the same profile_id and game already exists
    test = await document_crud.find_game_data(collection_name,profile.id,game)
    if test is not None:
        raise HTTPException(status_code=400,detail="Game data already exists, uploat it instead of creating a new one")

    game_data_mongodb = GameDataMongoDB(**game_data.model_dump(),
                                        game = game,
                                        profile_id_db = profile.id)
    
    game_data_temp = await document_crud.create_document(collection_name,game_data_mongodb)
    if game_data_temp is None:
        raise HTTPException(status_code=500,detail="Internal server error")

    if isinstance(game_data_temp, pymongo.results.InsertOneResult):
        game_data_id = game_data_temp.inserted_id
        return {"id": str(game_data_id)}
    print(**game_data_temp)
    game_data_db = GameDataMongoDB(id=str(game_data_temp["_id"]), **game_data_temp)

    return game_data_db


@router.get("/profiles/{profile_id_db}/game-data/{game}", summary="Get current user game data of a profile", description="This route allows you to get the current user game data.")
async def read_game_data(token: Annotated[str, Depends(oauth2_scheme)],profile_id_db:int,game: str, db = Depends(get_db_sql)):
    if not(game=="click" or game=="cursor"):
        raise HTTPException(status_code=400,detail="Invalid game type")
    
    current_user = await get_current_user(db,token)
    profile = await profile_verify(db,profile_id_db,current_user)

    result = await document_crud.find_game_data(collection_name,profile.id,game)

    if result is None:
        raise HTTPException(status_code=404,detail="Game data not found")
    
    return result["game_data"]


@router.put("/profiles/{profile_id_db}/game-data/{game}", summary="Update a game data", description="This route allows you to update a game data.")
async def update_game_data(token: Annotated[str, Depends(oauth2_scheme)],game_data: GameData,profile_id_db:int,game: str, db = Depends(get_db_sql)):
    if not(game=="click" or game=="cursor"):
        raise HTTPException(status_code=400,detail="Invalid game type")
    
    current_user = await get_current_user(db,token)
    profile = await profile_verify(db,profile_id_db,current_user)

    result = await document_crud.find_game_data(collection_name,profile.id,game)

    if result is None:
        raise HTTPException(status_code=404,detail="Game data not found")

    game_data_mongodb = GameDataMongoDB(**game_data.model_dump(),
                                        game = game,
                                        profile_id_db = profile.id)
    
    game_data_temp = await document_crud.update_document(collection_name,str(result["_id"]),game_data_mongodb)
    if game_data_temp is None:
        raise HTTPException(status_code=500,detail="Internal server error")
    
    if game_data_temp.modified_count == 1 or game_data_temp.matched_count == 1:
        return {"status": "success"}

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