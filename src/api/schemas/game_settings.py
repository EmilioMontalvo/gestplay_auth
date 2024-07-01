from typing import List, Any, Optional
from pydantic import BaseModel
from profile import Profile

class GameSettingsBase(BaseModel):
    profile_id: str
    active: bool
    alpha_opacity: int
    camera_id: int
    color: List[float]
    config_window_id: int
    contrl_window_size: List[int]
    control_computer_window_position: Optional[List[int]]
    cursor_id: int
    first_time: bool
    general_sound: int
    gesture_index: int
    music: int
    opacity: float
    pointer_smooth: int
    sfx: int
    size: int
    spd_down: int
    spd_left: int
    spd_right: int
    spd_up: int
    tick_interval_ms: int
    window_mode: int
    window_size_value: int

class GameSettingsCreate(GameSettingsBase):
    pass

class GameSettings(GameSettingsBase):
    id: int
    id_profile_db: int
    class Config:
        from_attributes = True
        arbitrary_types_allowed=True