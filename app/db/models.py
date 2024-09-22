#!/usr/bin/env python3

# file_name: models.py
# author: Gideon Oba
"""
Module contains SQLAlchemy database model schemas.
"""
from sqlalchemy import (
    Boolean, Column, DateTime,
    Integer, Float, String, Text,
    ForeignKey
)
from sqlalchemy.orm import relationship, backref, declarative_base
from datetime import datetime, timezone
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    role = Column(String, nullable=False, insert_default="user")
    memory_allocated = Column(Float, default=0.0)
    memory_used = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    # users relationships
    workspaces = relationship("Workspace", backref="admin", cascade="all, delete")
    alerts = relationship("Alert", backref="user", cascade="all, delete")


class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    admin_id = Column(String, ForeignKey('users.id'))
    total_memory = Column(Float, default=10.0)
    memory_used = Column(Float, default=0.0)
    max_users = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    # workspaces relationships
    users = relationship("WorkspaceUser", backref="workspace", cascade="all, delete")
    folders = relationship("Folder", backref="workspace", cascade="all, delete")
    invites = relationship("Invite", backref="workspace", cascade="all, delete")
    alerts = relationship("Alert", backref="workspace", cascade="all, delete")
    

class WorkspaceUser(Base):
    __tablename__ = "workspace_users"
    
    id = Column(String, primary_key=True)
    workspace_id = Column(String, ForeignKey("workspaces.id"))
    user_id = Column(String, ForeignKey("users.id"))
    role = Column(String, nullable=False) # "admin" or "user"
    memory_allocated = Column(Float, default=0.0) # memory allocated to user by admin
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    

class Folder(Base):
    __tablename__ = "folders"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id"))
    # user_id is nullable for admin folder
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    # parent_folder_id is nullable for nested folders
    parent_folder_id = Column(String, ForeignKey("folders.id"), nullable=True)
    is_root = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    # 1 is 1 relationship
    # Self-referencing relationship for nested folders
    subfolders = relationship('Folder', backref=backref("parent_folder", remote_side=[id]))
    

class File(Base):
    __tablename__ = 'files'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(Text, nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id"))
    user_id = Column(String, ForeignKey("users.id"))
    folder_id = Column(String, ForeignKey("folders.id"))
    size = Column(Float, nullable=False) # size in MB
    is_directory = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    update_at = Column(DateTime, default=datetime.now(timezone.utc))
    

class Invite(Base):
    __tablename__ = "invites"
    
    id = Column(String, primary_key=True)
    # e.g., "workspace_invite"
    invite_type = Column(String, nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id"))
    inviter_id = Column(String, ForeignKey("users.id"))
    invitee_email = Column(String, nullable=False)
    status = Column(String, default="pending") # invite status
    create_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    # Relationships
    inviter = relationship("User", backref="sent_invites")
    

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True)
    # e.g., "invite", "memory_usage", "memory_exceeded"
    alert_type = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id"))
    workspace_id = Column(String, ForeignKey("workspaces.id"))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
