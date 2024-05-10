from fastapi import APIRouter,HTTPException
from ..schemas.user import User,UserCreate,UserResponse,UserInDB

router = APIRouter(
    tags=["User Routes"]
)


@router.post("/users")
async def create_user(user_to_create: UserCreate) -> UserResponse:
    return {"message": "User created successfully"}