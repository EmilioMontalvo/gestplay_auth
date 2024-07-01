from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GameSettings(BaseModel):
    profile_id: str
    active: bool
    alpha_opacity: int
    camera_id: int
    color: List[float]
    config_window_id: int
    contrl_window_size: List[int]
    control_computer_window_position: Optional[Any]
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