import os
from typing import Annotated
from fastapi import Depends,APIRouter,HTTPException,status

from ..db import crud

from ..db.database import SessionLocal, engine
from ..db import models
from ..schemas.game_settings import GameSettings, GameSettingsCreate
from sqlalchemy.orm import Session
from ..schemas.user import User,UserCreate,UserBase
from ..utils.auth import get_current_user,oauth2_scheme
from ..schemas.email import Email as EmailSchema
from pydantic import EmailStr
from ..utils import token_generation as token_utils

models.Base.metadata.create_all(bind=engine) # create the tables in the database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    tags=["Game Settings Routes"]
)

# GameSettings routes

@router.post("/game_settings", summary="Create a new game settings", description="This route allows you to create a new game settings.")
async def create_game_settings(token: Annotated[str, Depends(oauth2_scheme)],game_settings: GameSettingsCreate,profile_id_db:int ,db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    profile=await profile_verify(db,profile_id_db,current_user)


    return crud.create_game_settings(db,game_settings,profile.id)


@router.get("/game_settings", summary="Get current user game settings of a profile", description="This route allows you to get the current user game settings.")
async def read_game_settings(token: Annotated[str, Depends(oauth2_scheme)],profile_id_db:int, db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    profile=await profile_verify(db,profile_id_db,current_user)

    return crud.get_game_settings_of_profile(db,profile.id)


@router.put("/game_settings", summary="Update current user game settings of a profile", description="This route allows you to update the current user game settings.")
async def update_game_settings(token: Annotated[str, Depends(oauth2_scheme)],game_settings: GameSettingsCreate,profile_id_db:int, db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    profile=await profile_verify(db,profile_id_db,current_user)
    settings = crud.get_game_settings_of_profile(db,profile.id)

    return crud.update_game_settings(db,game_settings,settings.id)



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

