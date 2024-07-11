from sqlalchemy.orm import Session
from . import models
from ..schemas.profile import ProfileBase as schemeProfile
from ..schemas.user import UserCreate
from ..schemas.game_settings import GameSettingsCreate as schemeGameSettings

#User Crud
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    #TODO: hash password
    hashed_password = user.password
    db_user = models.User(email=user.email, hashed_password=hashed_password, is_active=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: UserCreate, user_id: int):
    db_user = db.query(models.User).get(user_id)
    db_user.email = user.email
    db_user.hashed_password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

def set_last_used_profile(db: Session, user_id: int, profile_id: int):
    db_user:models.User = db.query(models.User).get(user_id)
    db_profile:models.Profile = db.query(models.Profile).get(profile_id)
    db_user.last_used_profile_id = db_profile.id
    db_user.last_used_profile=db_profile
    db.commit()
    db.refresh(db_user)
    return db_profile

def get_last_used_profile(db: Session, user_id: int):
    db_user = db.query(models.User).get(user_id)
    return db_user.last_used_profile

def get_user_last_token(db: Session, user_id: int,token:str):    
    return db.query(models.TokenTable).filter(models.TokenTable.user_id == user_id, models.TokenTable.access_toke==token).first()

# Profile CRUD
def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()

def create_profile_for_user(db: Session, profile: schemeProfile, user_id: int):
    user=db.query(models.User).get(user_id)
    db_profile = models.Profile(first_name=profile.first_name,
                                last_name=profile.last_name, 
                                image_path=profile.image_path, 
                                max_click_level=profile.max_click_level, 
                                max_cursor_level=profile.max_cursor_level)
    db.add(db_profile)
    print(db_profile)
    
    user.profiles.append(db_profile)


    db.commit()
    db.refresh(db_profile)
    db.refresh(user)
    return db_profile

def update_profile(db: Session, profile: schemeProfile, profile_id: int):
    db_profile = db.query(models.Profile).get(profile_id)
    db_profile.first_name = profile.first_name
    db_profile.last_name = profile.last_name
    db_profile.image_path = profile.image_path
    db_profile.max_click_level = profile.max_click_level
    db_profile.max_cursor_level = profile.max_cursor_level
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_profiles_of_user(db: Session, user_id: int):
    user=db.query(models.User).get(user_id)
    return user.profiles

def assing_profile_to_user(db: Session, profile_id: int, user_id: int):
    db_user = db.query(models.User).get(user_id)
    db_profile = db.query(models.Profile).get(profile_id)
    db_user.profiles.append(db_profile)
    db.commit()
    db.refresh(db_user)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    db_profile = db.query(models.Profile).get(profile_id)
    db.delete(db_profile)
    db.commit()
    return db_profile

def detach_profile_from_user(db: Session, profile_id: int, user_id: int):
    db_user = db.query(models.User).get(user_id)
    db_profile = db.query(models.Profile).get(profile_id)
    db_user.profiles.remove(db_profile)
    db.commit()
    db.refresh(db_user)
    return db_profile

def get_profile_if_user_owns_profile(db: Session, profile_id: int, user_id: int):
    
    ur_profiles=get_profiles_of_user(db, user_id)
    db_profile = db.query(models.Profile).get(profile_id)

    if db_profile in ur_profiles and db_profile is not None:
        return db_profile
    else:
        return None

def profile_exists(db: Session, profile_id: int):
    return db.query(models.Profile).get(profile_id) is not None


# GameSettings CRUD
def get_game_settings_of_profile(db: Session, profile_id: int):
    return db.query(models.GameSettings).filter(models.GameSettings.profile_id_db==profile_id).first()

def get_game_settings_by_profile_id(db: Session, profile_id: int):
    return db.query(models.GameSettings).filter(models.GameSettings.profile_id_db == profile_id).first()

def create_game_settings(db: Session, game_settings:schemeGameSettings, profile_id_db:int):

    db_game_settings = models.GameSettings(profile_id_db=profile_id_db,
                                            profile_id=game_settings.profile_id,
                                            active=game_settings.active,
                                            alpha_opacity=game_settings.alpha_opacity,
                                            camera_id=game_settings.camera_id,
                                            color=game_settings.color,
                                            config_window_id=game_settings.config_window_id,
                                            contrl_window_size=game_settings.contrl_window_size,
                                            control_computer_window_position=game_settings.control_computer_window_position,
                                            cursor_id=game_settings.cursor_id,
                                            first_time=game_settings.first_time,
                                            general_sound=game_settings.general_sound,
                                            gesture_index=game_settings.gesture_index,
                                            music=game_settings.music,
                                            opacity=game_settings.opacity,
                                            pointer_smooth=game_settings.pointer_smooth,
                                            sfx=game_settings.sfx,
                                            size=game_settings.size,
                                            spd_down=game_settings.spd_down,
                                            spd_left=game_settings.spd_left,
                                            spd_right=game_settings.spd_right,
                                            spd_up=game_settings.spd_up,
                                            tick_interval_ms=game_settings.tick_interval_ms,
                                            window_mode=game_settings.window_mode,
                                            window_size_value=game_settings.window_size_value)
    
    db.add(db_game_settings)
    db.commit()
    db.refresh(db_game_settings)
    return db_game_settings

def update_game_settings(db: Session, game_settings: dict, game_settings_id: int):
    db_game_settings: models.GameSettings = db.query(models.GameSettings).get(game_settings_id)
    
    # Iterar sobre los elementos del diccionario y actualizar solo los valores presentes
    for key, value in game_settings.items():
        if hasattr(db_game_settings, key):
            setattr(db_game_settings, key, value)
    
    db.commit()
    db.refresh(db_game_settings)
    return db_game_settings


    db.commit()
    db.refresh(db_game_settings)
    return db_game_settings
