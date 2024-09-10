#!/usr/bin/env python3

# file_name: models.py
# author: Gideon Oba
"""
Module contains SQLAlchemy database model schemas.
"""
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """
    Schema User contains user's details

    User schema attributes:

    - id: integer, primary key
    - username: string, not null
    - hashed_password: string, not null
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
