from pydantic import BaseModel

class GameProfile(BaseModel):
    id: str
    user_id: str  # Nuevo campo para identificar el usuario al que pertenece el perfil
    first_name: str
    last_name: str
    image_path: str
    max_click_level: int
    max_cursor_level: int
