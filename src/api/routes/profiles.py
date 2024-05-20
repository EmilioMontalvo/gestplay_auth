from typing import Annotated
from fastapi import Depends,APIRouter,HTTPException,status
from ..database import SessionLocal, engine
from .. import crud,models
from ..schemas.profile import Profile, ProfileCreate
from sqlalchemy.orm import Session
from ..schemas.user import User,UserCreate,UserBase
from ..utils.auth import get_current_user,oauth2_scheme

models.Base.metadata.create_all(bind=engine) # create the tables in the database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    tags=["Profile Routes"]
)


@router.post("/profiles/me", summary="Create a new profile", description="This route allows you to create a new profile.")
async def create_profiles(token: Annotated[str, Depends(oauth2_scheme)],profile: ProfileCreate ,db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)
    profile_to_create=Profile(id=0,name=profile.name)    
    return crud.create_profile_for_user(db,profile_to_create,current_user.id)

@router.get("/profiles/me", summary="Get current user profile", description="This route allows you to get the current user profile.")
async def read_profiles_me(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    return crud.get_profiles_of_user(db,current_user.id)
