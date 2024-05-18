from sqlalchemy import Table,Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

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
    name = Column(String, index=True)

    tutors = relationship("User", secondary=user_profile_association, back_populates='profiles')