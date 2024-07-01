from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.game_profile import GameProfile, GameProfileInDB
from ..schemas.user import User
from ..utils.auth import get_current_user, oauth2_scheme
from typing import Annotated
from ..database import SessionLocal, engine
from sqlalchemy.orm import Session
from bson.objectid import ObjectId
from ..db.document_crud import create_document, delete_document, find_document, update_document
import pymongo

router = APIRouter(
    tags=["Game Profile Routes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

collection_name = "game_profiles"

@router.post("/game_profile/")
async def create_game_profile(
        profile: GameProfile, 
        token: Annotated[str, Depends(oauth2_scheme)], 
        db: Session = Depends(get_db)
    ):
    current_user: User = await get_current_user(db, token)

    profile.user_id = current_user.id

    profile_temp=await create_document(collection_name,profile)

    if isinstance(profile_temp, pymongo.results.InsertOneResult):
        profile_id = profile_temp.inserted_id
        return {"id": str(profile_id)}
    
    profile_db = GameProfileInDB(id=str(profile_temp["_id"]), gameProfile=profile_temp)