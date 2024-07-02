from sqlalchemy import Table,Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, Boolean, String, ForeignKey
from .database import Base
from sqlalchemy.dialects.postgresql import ARRAY

user_profile_association = Table(
    "user_profile_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("profile_id", Integer, ForeignKey("profiles.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    profiles = relationship("Profile",secondary=user_profile_association, back_populates='tutors')

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    local_id = Column(String, index=True)
    name = Column(String, index=True)    
    last_name = Column(String, index=True) 
    image_path = Column(String, index=True) 
    max_click_level = Column(Integer, index=True) 
    max_cursor_level = Column(Integer, index=True) 

    tutors = relationship("User", secondary=user_profile_association, back_populates='profiles')

class GameSettings(Base):
    __tablename__ = 'game_settings'

    id = Column(Integer, primary_key=True, index=True)
    profile_id_db = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    profile_id = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)
    alpha_opacity = Column(Integer, nullable=False)
    camera_id = Column(Integer, nullable=False)
    color = Column(ARRAY(Float), nullable=False)
    config_window_id = Column(Integer, nullable=False)
    contrl_window_size = Column(ARRAY(Integer), nullable=False)
    control_computer_window_position = Column(ARRAY(Integer), nullable=True)
    cursor_id = Column(Integer, nullable=False)
    first_time = Column(Boolean, nullable=False)
    general_sound = Column(Integer, nullable=False)
    gesture_index = Column(Integer, nullable=False)
    music = Column(Integer, nullable=False)
    opacity = Column(Float, nullable=False)
    pointer_smooth = Column(Integer, nullable=False)
    sfx = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    spd_down = Column(Integer, nullable=False)
    spd_left = Column(Integer, nullable=False)
    spd_right = Column(Integer, nullable=False)
    spd_up = Column(Integer, nullable=False)
    tick_interval_ms = Column(Integer, nullable=False)
    window_mode = Column(Integer, nullable=False)
    window_size_value = Column(Integer, nullable=False)

    profile = relationship('Profile', uselist=False)


