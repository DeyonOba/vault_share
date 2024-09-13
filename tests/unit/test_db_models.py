"""
Unittest for database model schemas.

    - Users
    - ...
"""
import unittest
from app.db.models import User
from sqlalchemy import Integer, String, UniqueConstraint
from typing import Dict, Union


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

 
class TestUserSchema(unittest.TestCase):        
    def test_table_name(self):
        self.assertEqual(User.__tablename__, "users")
    
    def test_attribute_names_update(self):
        tested_columns = ["id", "username", "hashed_password", "role"]
        qualname = ".".join([__name__, self.__class__.test_attribute_names_update.__qualname__])
        self.assertListEqual(
            tested_columns, User.__table__.columns.keys(),
            msg=f"Add schema attribute testcase to class <{self.__class__.__name__}> and update <{qualname}>"
            )

    def test_table_attributes(self):
        check_column(self, User, 'id', Integer, nullable=False)
        check_column(self, User, 'username', String, nullable=False, length=250)
        check_column(self, User, 'hashed_password', String, nullable=False, length=250)
        check_column(self, User, 'role', String, nullable=False)
    
    def test_primary_key(self):
        primary_keys = [key.name for key in User.__table__.primary_key]
        self.assertIn('id', primary_keys, 'id should be a primary key')

    def test_unique_columns(self):
        unique_col = UniqueConstraint(User.__table__.columns["username"])
        self.assertIn(unique_col, User.__table__.constraints)

if __name__ == "__main__":
    unittest.main(verbose=2)
