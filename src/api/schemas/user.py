from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    is_active: bool

    model_config = {"json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "johndoe",
                    "email": "johndoe@example.com",
                    "password": "password",
                    "is_active": True
                }
            ]
        }
    }

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    model_config = {"json_schema_extra": {
            "examples": [
                {
                    "username": "johndoe",
                    "email": "johndoe@example.com",
                    "password": "password"
                }
            ]
        }
    }

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    model_config = {"json_schema_extra": {
            "examples": [
                {
                    "username": "johndoe",
                    "email": "johndoe@example.com",
                    
                }
            ]
        }
    }


class UserInDB(User):
    hashed_password: str


    