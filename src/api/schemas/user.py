from pydantic import BaseModel, EmailStr, field_validator
from profile import Profile
import re


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, value):
        """
        Valida la política de contraseñas:
        - Al menos 8 caracteres
        - Máximo 128 caracteres
        - Al menos una letra mayúscula
        - Al menos una letra minúscula
        - Al menos un número
        - Al menos un carácter especial
        """
        if not re.search(r'[A-Z]', value):
            raise ValueError('La contraseña debe tener al menos una letra mayúscula.')
        if not re.search(r'[a-z]', value):
            raise ValueError('La contraseña debe tener al menos una letra minúscula.')
        if not re.search(r'\d', value):
            raise ValueError('La contraseña debe tener al menos un número.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('La contraseña debe tener al menos un carácter especial.')
        return value
        

class User(UserBase):
    id: int
    is_active: bool
    profiles: list[Profile]
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed=True
        


    