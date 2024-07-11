from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, ARRAY, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    last_used_profile_id = Column(Integer, ForeignKey('profiles.id',ondelete='SET NULL'))

    profiles = relationship("Profile", back_populates='user', foreign_keys='Profile.user_id', cascade="all")
    last_used_profile = relationship("Profile", uselist=False, foreign_keys=[last_used_profile_id])

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)    
    last_name = Column(String, index=True) 
    image_path = Column(String, index=True) 
    max_click_level = Column(Integer, index=True) 
    max_cursor_level = Column(Integer, index=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    game_settings = relationship("GameSettings", uselist=False, back_populates='profile', cascade="all, delete-orphan",passive_deletes=True)
    user = relationship("User", back_populates='profiles', foreign_keys=[user_id])

class GameSettings(Base):
    __tablename__ = 'game_settings'

    id = Column(Integer, primary_key=True, index=True)
    profile_id_db = Column(Integer, ForeignKey('profiles.id',ondelete='CASCADE'), nullable=False)
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
    general_sound = Column(Float, nullable=False)
    gesture_index = Column(Integer, nullable=False)
    music = Column(Float, nullable=False)
    opacity = Column(Float, nullable=False)
    pointer_smooth = Column(Integer, nullable=False)
    sfx = Column(Float, nullable=False)
    size = Column(Integer, nullable=False)
    spd_down = Column(Integer, nullable=False)
    spd_left = Column(Integer, nullable=False)
    spd_right = Column(Integer, nullable=False)
    spd_up = Column(Integer, nullable=False)
    tick_interval_ms = Column(Integer, nullable=False)
    window_mode = Column(Integer, nullable=False)
    window_size_value = Column(Integer, nullable=False)

    profile = relationship('Profile', uselist=False)

class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now())
