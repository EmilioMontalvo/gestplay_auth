from fastapi import APIRouter,HTTPException
from ..schemas.user import User,UserCreate,UserResponse,UserInDB

router = APIRouter(
    tags=["User Routes"]
)


@router.post("/register", response_model=UserResponse, summary="Register a new user", description="This route allows you to register a new user.")
async def register(user_to_create: UserCreate) -> UserResponse:
    return {"message": "User created successfully"}