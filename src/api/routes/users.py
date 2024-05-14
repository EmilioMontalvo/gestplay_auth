from fastapi import Depends,APIRouter,HTTPException
from ..schemas.user import User,UserCreate,UserBase
from .. import crud,models
from ..database import SessionLocal, engine
from sqlalchemy.orm import Session

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
    
    created_user = crud.create_user(db, user_to_create)
    
    user_to_return=UserBase(email=created_user.email)

    return user_to_return