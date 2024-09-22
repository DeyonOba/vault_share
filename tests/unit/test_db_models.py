"""
Unittest for database model schemas.

    - Users
    - ...
"""
import unittest
from app.db.models import User, Workspace
from sqlalchemy import Integer, DateTime, String, Float, UniqueConstraint
from typing import Dict, Union

EXPECTED_USER_COLUMNS = [
    "id", "username", "hashed_password", "role",
    "memory_allocated", "memory_used", "created_at"
]
EXPECTED_WORKSPACE_COLUMNS = [
    "id", "name", "admin_id", "total_memory",
    "memory_used", "max_users", "created_at"
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
        check_column(self, User, 'username', String, nullable=False, length=250)
        check_column(self, User, 'hashed_password', String, nullable=False, length=250)
        check_column(self, User, 'role', String, nullable=False)
        check_column(self, User, 'memory_allocated', Float)
        check_column(self, User, "memory_used", Float)
        check_column(self, User, "created_at", DateTime)
    
    def test_primary_key(self):
        verify_primary_keys(self, User, "id")

    def test_unique_columns(self):
        unique_col = UniqueConstraint(User.__table__.columns["username"])
        self.assertIn(unique_col, User.__table__.constraints)


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
