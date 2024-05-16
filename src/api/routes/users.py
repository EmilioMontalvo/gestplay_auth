from datetime import timedelta
from typing import Annotated
from fastapi import Depends,APIRouter,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.user import User,UserCreate,UserBase
from ..schemas.token import Token
from .. import crud,models
from ..database import SessionLocal, engine
from sqlalchemy.orm import Session
from ..utils.auth import authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,get_current_user,get_password_hash,oauth2_scheme

models.Base.metadata.create_all(bind=engine) # create the tables in the database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["User Routes"]
)


@router.post("/register", response_model=UserBase, summary="Register a new user", description="This route allows you to register a new user.")
async def register(user_to_create: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = crud.get_user_by_email(db, email=user_to_create.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_to_create.password = get_password_hash(user_to_create.password)
    created_user = crud.create_user(db, user_to_create)    
    user_to_return=UserBase(email=created_user.email)

    return user_to_return

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=UserBase, summary="Get current user", description="This route allows you to get the current user.")
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    
    current_user: User= await get_current_user(db,token)
    user_to_return=UserBase(email=current_user.email)

    return user_to_return