from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Annotated
from ..schemas.token import TokenData
from sqlalchemy.orm import Session
from ..db.crud import get_user_by_email
from ..db import crud
from ..schemas.user import User
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(Database,token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception
    

    user = get_user_by_email(Database, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    token = crud.get_user_last_token(Database,user.id,token)

    if token is None:
        raise credentials_exception
    
    if token.status == False:
        raise credentials_exception

    return user

def authenticate_user(Database, email: str, password: str):
    user = get_user_by_email(Database, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

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