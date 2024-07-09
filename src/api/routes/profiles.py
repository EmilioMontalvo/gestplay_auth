import os
from typing import Annotated
from fastapi import Depends,APIRouter,HTTPException,status,BackgroundTasks,UploadFile,File

from ..db import crud
from ..db import document_crud

from ..utils.email import send_email
from ..db.database import SessionLocal, engine
from ..db import models
from ..schemas.profile import Profile, ProfileCreate,ProfileBase
from ..schemas.game_settings import GameSettings, GameSettingsCreate
from ..schemas.game_data import GameData
from ..routes.game_data import create_game_data
from ..routes.game_settings import create_game_settings

from sqlalchemy.orm import Session
from ..schemas.user import User,UserCreate,UserBase
from ..utils.auth import get_current_user,oauth2_scheme,profile_verify
from ..schemas.email import Email as EmailSchema
from pydantic import EmailStr
from ..utils import token_generation as token_utils


models.Base.metadata.create_all(bind=engine) # create the tables in the database
collection_name = "game_data"

default_game_settings = GameSettingsCreate(
    profile_id="-1",
    window_mode=0,
    general_sound=1,
    music=1,
    sfx=1,
    control_computer_window_position=None,
    first_time=True,
    config_window_id=1,
    contrl_window_size=[362, 475],
    window_size_value=0,
    alpha_opacity=255,
    camera_id=0,
    gesture_index=0,
    spd_up=10,
    spd_down=10,
    spd_left=10,
    spd_right=10,
    pointer_smooth=65,
    tick_interval_ms=16,
    cursor_id=3,
    size=100,
    opacity=0.5,
    color=[0.3098, 0.639, 0.866, 1],
    active=True
)

default_cursor_game_data = GameData(
    profile_id="-1",
    game_data={
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": []
    }
)

default_click_game_data = GameData(
    profile_id="-1",
    game_data={
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": []
    }
)

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
async def create_profiles(token: Annotated[str, Depends(oauth2_scheme)],profile: ProfileCreate , background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)
    profile_to_create=ProfileBase(                       
                              first_name=profile.first_name,
                              last_name=profile.last_name,
                              image_path=profile.image_path,
                              max_click_level=profile.max_click_level,
                              max_cursor_level=profile.max_cursor_level
                              )
    
    
    created_profile=crud.create_profile_for_user(db,profile_to_create,current_user.id)

    if not created_profile:
        raise HTTPException(status_code=500,detail="An error occurred while creating the profile")
    
    # add default game settings for the profile
    default_cursor_game_data.profile_id = str(created_profile.id)
    default_click_game_data.profile_id = str(created_profile.id)
    default_game_settings.profile_id = str(created_profile.id)

    background_tasks.add_task(create_game_settings, token, default_game_settings, created_profile.id, db)
    background_tasks.add_task(create_game_data, token, default_cursor_game_data, created_profile.id, "cursor", db)
    background_tasks.add_task(create_game_data, token, default_click_game_data, created_profile.id, "click", db)


    return created_profile

@router.get("/profiles/me", summary="Get current user profiles", description="This route allows you to get the user profile s.")
async def read_profiles_me(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    return crud.get_profiles_of_user(db,current_user.id)

#share profile
@router.post("/profiles/share", summary="Share a profile", description="This route allows you to share a profile with another user.")
async def share_profile(token: Annotated[str, Depends(oauth2_scheme)],profile_id:int, email:EmailStr, db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    


    if not crud.profile_exists(db,profile_id):
        raise HTTPException(status_code=404,detail="Profile not found")
    
    if not crud.get_profiles_of_user(db,current_user.id):
        raise HTTPException(status_code=400,detail="You don't have any profiles to share")
    
    profile_to_share=crud.get_profile_if_user_owns_profile(db,profile_id=profile_id,user_id=current_user.id)
    if not profile_to_share:
        raise HTTPException(status_code=403,detail="You don't own this profile")

    if current_user.email==email:
        raise HTTPException(status_code=400,detail="You can't share a profile with yourself")

    mail_schema = EmailSchema(email=[email])

    
    mail_dict = {
        "link": f"{os.getenv("Frontend_URL")}/share-profile/{token_utils.profile_token(Profile(id=profile_to_share.id,first_name=profile_to_share.name),email=email)}/",
        "sender":current_user.email,
        "register":f"{os.getenv("Frontend_URL")}/register/"
    }

    result=await send_email(mail_schema, body=mail_dict,template="share_profile.html",subject="A user has shared a profile with you")

    if result:
        return {"message":"Email sent"}
    else:
        raise HTTPException(status_code=500,detail="An error occurred while sharing the profile")
    
#get profile by id
@router.get("/profiles/me/{profile_id_db}", summary="Get a profile", description="This route allows you to get a profile.")
async def read_profile(token: Annotated[str, Depends(oauth2_scheme)],profile_id_db:int, db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    profile=await profile_verify(db,profile_id_db,current_user)

    return profile


@router.put("/profiles/me/{profile_id_db}", summary="Update a profile", description="This route allows you to update a profile.")
async def update_profile(token: Annotated[str, Depends(oauth2_scheme)],profile_id_db:int,profile: ProfileCreate, db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    profile_to_update=await profile_verify(db,profile_id_db,current_user)

    updated_profile=crud.update_profile(db,profile,profile_to_update.id)

    if not updated_profile:
        raise HTTPException(status_code=500,detail="An error occurred while updating the profile")

    return updated_profile

#set profile image
@router.put("/profiles/me/{profile_id_db}/image", summary="Set profile image", description="This route allows you to set the profile image.")
async def update_profile_image(token: Annotated[str, Depends(oauth2_scheme)],profile_id_db:int,file: UploadFile=File(...), db: Session = Depends(get_db)):
    
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG and JPEG images are allowed.")
    
    
    current_user: User= await get_current_user(db,token)

    profile_to_update=await profile_verify(db,profile_id_db,current_user)

    profile_to_update.image_path="hola"
    
    updated_profile=crud.update_profile(db,profile_to_update,profile_to_update.id)



    if not updated_profile:
        raise HTTPException(status_code=500,detail="An error occurred while updating the profile image")

    return updated_profile
    

@router.get("/profiles/assign/{token}", summary="Assign a profile", description="This route allows you to assign a profile to a user.")
async def assign_profile(token:str, db: Session = Depends(get_db)):
    token_data = token_utils.verify_profile_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail= "Token for Profile share has expired."
        )
    user = db.query(models.User).filter(models.User.email==token_data['email']).first()
    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"User with email {user.email} does not exist"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Account Not Verified"
        )
    
    print(token_data)
    crud.assing_profile_to_user(db,profile_id=token_data['id'],user_id=user.id)

    return {
        'message':'Profile assigned Successfuly',
        'status':status.HTTP_202_ACCEPTED
    }

@router.delete("/profiles/{profile_id}", summary="Delete a profile", description="This route allows you to delete a profile.")
async def delete_profile(token: Annotated[str, Depends(oauth2_scheme)],profile_id:int, db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)
    profile=await profile_verify(db,profile_id,current_user)

    response=crud.delete_profile(db,profile.id)

    if not response:
        raise HTTPException(status_code=500,detail="An error occurred while deleting the profile")
    
    delete_game_data_cursor = await document_crud.delete_game_data(collection_name,profile.id,"cursor")
    delete_game_data_click = await document_crud.delete_game_data(collection_name,profile.id,"click")
    if not delete_game_data_cursor:
        raise HTTPException(status_code=500,detail="An error occurred while deleting the game data")
    
    if not delete_game_data_click:
        raise HTTPException(status_code=500,detail="An error occurred while deleting the game data")
    

    return response

#get last used profile
@router.get("/profiles/last", summary="Get last used profile", description="This route allows you to get the last used profile.")
async def read_last_profile(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)

    last_used_profile=crud.get_last_used_profile(db,current_user.id)

    if last_used_profile is None:
        raise HTTPException(status_code=404,detail="There is no last used profile")

    return last_used_profile

#set last used profile
@router.put("/profiles/last", summary="Set last used profile", description="This route allows you to set the last used profile.")
async def update_last_profile(token: Annotated[str, Depends(oauth2_scheme)],profile_id:int, db: Session = Depends(get_db)):
    current_user: User= await get_current_user(db,token)
    profile=await profile_verify(db,profile_id,current_user)

    return crud.set_last_used_profile(db,profile.id,current_user.id)


