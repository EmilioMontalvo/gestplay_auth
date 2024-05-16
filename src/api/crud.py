from sqlalchemy.orm import Session
from . import models
from .schemas.profile import Profile as schemeProfile
from .schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    #TODO: hash password
    print(user)
    hashed_password = user.password
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()

def create_profile_for_user(db: Session, profile: schemeProfile, user_id: int):
    db_profile = models.Profile(**profile.model_dump(), tutors=[models.User(id=user_id)])
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profiles_of_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).all()