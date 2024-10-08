"""
Unittest for database model schemas. Test module ensure that schema
schema satisfies the outlined app business logic.

    - Users
    - Workspace
    - WorkspaceUser
    - Folder
    - File
    - Invite
    - Alert
"""
import unittest
from vaultShare.db.models import User, Workspace, WorkspaceUser, Folder, File, Invite, Alert
from sqlalchemy import Integer, Boolean, DateTime, String, Float, UniqueConstraint
from typing import Dict, Union

EXPECTED_USER_COLUMNS = [
    "id", "email", "username", "hashed_password", "role",
    "memory_allocated", "memory_used", "session_id", "created_at",
]
EXPECTED_WORKSPACE_COLUMNS = [
    "id", "name", "admin_id", "total_memory",
    "memory_used", "max_users", "created_at"
]
EXPECTED_WORKSPACEUSER_COLUMNS = [
    "id", "workspace_id", "user_id", "role",
    "memory_allocated", "created_at"
]
EXPECTED_FOLDER_COLUMNS = [
    "id", "name", "workspace_id", "user_id",
    "parent_folder_id", "is_root", "created_at"
]
EXPECTED_FILE_COLUMNS = [
    "id", "name", "path", "workspace_id",
    "user_id", "folder_id", "size", "is_directory",
    "created_at", "updated_at"
]
EXPECTED_INVITE_COLUMNS = [
    "id", "invite_type", "workspace_id", "inviter_id",
    "invitee_email", "status", "created_at"
]
EXPECTED_ALERT_COLUMNS = [
    "id", "alert_type", "user_id", "workspace_id",
    "message", "is_read", "created_at"
]

def verify_table_name(obj, model, table_name):
    obj.assertEqual(model.__tablename__, table_name)

def check_column(
    obj, model, column_name, expected_dtype, 
    nullable=True, length=None
):
    column = model.__table__.columns.get(column_name)
    
    # Check if the column exists
    obj.assertIsNotNone(column, f"column: {column_name} is missing")
    
    # Check if column type matches the expected type
    obj.assertIsInstance(
        column.type, expected_dtype,
        msg=f"{column_name} should be of type {expected_dtype}"
    )
    
    # Check the nullable property
    obj.assertEqual(
        column.nullable, nullable,
        f"{column_name} nullable should be {nullable}"
    )
    
    # Check String type property length
    if length is not None:
        obj.assertEqual(
            column.type.length, length,
            f"{column_name} length should be {length}"
        )

def verify_primary_keys(obj, model, col_name):
    primary_keys = [key.name for key in model.__table__.primary_key]
    obj.assertIn(
        col_name, primary_keys,
        f"{col_name} should be a primary key"
    )
    
def verify_expected_attribute_names(obj, model, col_names: list):
    qualname = ".".join([__name__, obj.__class__.test_attribute_names_update.__qualname__])
    error_msg = f"Add schema attribute testcase to class <{obj.__class__.__name__}> and update <{qualname}>"
    obj.assertListEqual(
        col_names, model.__table__.columns.keys(),
        msg=error_msg
    )

 
class TestUserSchema(unittest.TestCase):        
    def test_table_name(self):
        verify_table_name(self, User, "users")
    
    def test_attribute_names_update(self):
        verify_expected_attribute_names(self, User, EXPECTED_USER_COLUMNS)

    def test_table_attributes(self):
        check_column(self, User, 'id', String, nullable=False)
        check_column(self, User, 'username', String, nullable=False, length=None)
        check_column(self, User, "email", String, nullable=False)
        check_column(self, User, 'hashed_password', String, nullable=False, length=None)
        check_column(self, User, 'role', String, nullable=False)
        check_column(self, User, 'memory_allocated', Float)
        check_column(self, User, "memory_used", Float)
        check_column(self, User, "session_id", String)
        check_column(self, User, "created_at", DateTime)
    
    def test_primary_key(self):
        verify_primary_keys(self, User, "id")

    def test_unique_columns(self):
        unique_col_id = UniqueConstraint(User.__table__.columns["id"])
        unique_col_email = UniqueConstraint(User.__table__.columns["email"])
        
        self.assertIn(unique_col_id, User.__table__.constraints)
        self.assertIn(unique_col_email, User.__table__.constraints)


class TestWorkspaceSchema(unittest.TestCase):
    def test_table_name(self):
        verify_table_name(self, Workspace, "workspaces")

    def test_attribute_names_update(self):
        verify_expected_attribute_names(self, Workspace, EXPECTED_WORKSPACE_COLUMNS)

    def test_table_attributes(self):
        check_column(self, Workspace, "id", String, nullable=False)
        check_column(self, Workspace, "name", String, nullable=False)
        check_column(self, Workspace, "admin_id", String, nullable=False)
        check_column(self, Workspace, "total_memory", Float)
        check_column(self, Workspace, "memory_used", Float)
        check_column(self, Workspace, "max_users", Integer)
        check_column(self, Workspace, "created_at", DateTime)

    def test_primary_key(self):
        verify_primary_keys(self, Workspace, "id")


class TestWorkspaceUserSchema(unittest.TestCase):
    def test_table_name(self):
        verify_table_name(self, WorkspaceUser, "workspace_users")
        
    def test_attribute_names_update(self):
        verify_expected_attribute_names(self, WorkspaceUser, EXPECTED_WORKSPACEUSER_COLUMNS)
    
    def test_table_attributes(self):
        check_column(self, WorkspaceUser, "id", String, nullable=False)
        check_column(self, WorkspaceUser, "workspace_id", String, nullable=False)
        check_column(self, WorkspaceUser, "user_id", String, nullable=False)
        check_column(self, WorkspaceUser, "role", String, nullable=False)
        check_column(self, WorkspaceUser, "memory_allocated", Float)
        check_column(self, WorkspaceUser, "created_at", DateTime)
        
    def test_primary_key(self):
        verify_primary_keys(self, WorkspaceUser, "id")


class TestFolderSchema(unittest.TestCase):
    def test_table_name(self):
        verify_table_name(self, Folder, "folders")
    
    def test_attribute_names_update(self):
        verify_expected_attribute_names(self, Folder, EXPECTED_FOLDER_COLUMNS)
    
    def test_table_attributes(self):
        check_column(self, Folder, "id", String, nullable=False)
        check_column(self, Folder, "name", String, nullable=False)
        check_column(self, Folder, "workspace_id", String, nullable=False)
        check_column(self, Folder, "user_id", String)
        check_column(self, Folder, "parent_folder_id", String)
        check_column(self, Folder, "is_root", Boolean)
        check_column(self, Folder, "created_at", DateTime)
        
    def test_primary_key(self):
        verify_primary_keys(self, Folder, "id")
        

class TestFileSchema(unittest.TestCase):
    def test_table_name(self):
        verify_table_name(self, File, "files")
    
    def test_attribute_names_update(self):
        verify_expected_attribute_names(self, File, EXPECTED_FILE_COLUMNS)
           
    def test_table_attributes(self):
        check_column(self, File, "id", String, nullable=False)
        check_column(self, File, "name", String, nullable=False)
        check_column(self, File, "workspace_id", String, nullable=False)
        check_column(self, File, "user_id", String)
        check_column(self, File, "folder_id", String)
        check_column(self, File, "size", Float, nullable=False)
        check_column(self, File, "is_directory", Boolean)
        check_column(self, File, "created_at", DateTime)
        check_column(self, File, "updated_at", DateTime)
        
    def test_primary_key(self):
        verify_primary_keys(self, File, "id")


class TestInviteSchema(unittest.TestCase):
    def test_table_name(self):
        verify_table_name(self, Invite, "invites")
        
    def test_attribute_names_update(self):
        verify_expected_attribute_names(self, Invite, EXPECTED_INVITE_COLUMNS)
           
    def test_table_attributes(self):
        check_column(self, Invite, "id", String, nullable=False)
        check_column(self, Invite, "invite_type", String, nullable=False)
        check_column(self, Invite, "workspace_id", String, nullable=False)
        check_column(self, Invite, "inviter_id", String, nullable=False)
        check_column(self, Invite, "invitee_email", String, nullable=False)
        check_column(self, Invite, "status", String)
        check_column(self, Invite, "created_at", DateTime)
        
    def test_primary_key(self):
        verify_primary_keys(self, Invite, "id")

class TestAlertSchema(unittest.TestCase):
    def test_table_name(self):
        verify_table_name(self, Alert, "alerts")
    
    def test_attribute_names_update(self):
        verify_expected_attribute_names(self, Alert, EXPECTED_ALERT_COLUMNS)
        
    def test_table_attributes(self):
        check_column(self, Alert, "id", String, nullable=False)
        check_column(self, Alert, "alert_type", String, nullable=False)
        check_column(self, Alert, "user_id", String, nullable=False)
        check_column(self, Alert, "workspace_id", String)
        check_column(self, Alert, "message", String, nullable=False)
        check_column(self, Alert, "is_read", Boolean)
        check_column(self, Alert, "created_at", DateTime)
        
    def test_primary_key(self):
        verify_primary_keys(self, Alert, "id")
