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
    general_sound: float
    gesture_index: int
    music: float
    opacity: float
    pointer_smooth: int
    sfx: float
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


# Properties to receive on item update (they are optional)
class GameSettingsUpdate(BaseModel):
    alpha_opacity: Optional[int]=None
    camera_id: Optional[int] = None
    color: Optional[List[float]] = None
    config_window_id: Optional[int] = None
    contrl_window_size: Optional[List[int]] = None
    control_computer_window_position: Optional[List[int]] = None
    cursor_id: Optional[int] = None 
    first_time: Optional[bool] = None
    general_sound: Optional[float] = None
    gesture_index: Optional[int] = None
    music: Optional[float] = None
    opacity: Optional[float] = None
    pointer_smooth: Optional[int] = None
    sfx: Optional[float] = None
    size: Optional[int] = None
    spd_down: Optional[int] = None
    spd_left: Optional[int] = None
    spd_right: Optional[int] = None
    spd_up: Optional[int] = None
    tick_interval_ms: Optional[int] = None
    window_mode: Optional[int] = None
    window_size_value: Optional[int] = None


class GameSettings(GameSettingsBase):
    id: int
    id_profile_db: int
    class Config:
        from_attributes = True
        arbitrary_types_allowed=True