"""
Test database interactions using the DB class.
"""
import unittest
from unittest.mock import patch, MagicMock
from app.db.models import User
from app.db.db import DB
from parameterized import parameterized
from sqlalchemy.exc import SQLAlchemyError

class TestDBModule(unittest.TestCase):
    """Test DB class."""
    def setUp(self):
        """Set up a DB instance with a mock database URL."""
        self.db = DB(database_url="sqlite:///:memory:", echo=False)
    
    @parameterized.expand([
        ("Bob_Dylan", "bob_dylan", "awesomeBob", None),
        ("John_Doe", "john_doe", "justGiveMeAcess", None),
        ("Dev_Success", "dev_success", "PassWord", "admin"),
    ])   
    @patch("app.db.db.DB._session", new_callable=MagicMock)
    def test_add_user_success(self, _, username, password, role, mock_session):
        """Test if user is added to database."""
        # Mock the add and commit behavior
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        
        if role is None:
            user = self.db.add_user(username, password, role="user")
        else:
            user = self.db.add_user(username, password, role=role)
        
        # Assert that a User object was returned
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, username)
        self.assertEqual(user.hashed_password, password)
        
        if role is None:
            self.assertEqual(user.role, "user")
        else:
            self.assertEqual(user.role, role)
        
        # Assert that the session's add and commit methods were called
        mock_session.add.assert_called_once_with(user)
        mock_session.commit.assert_called_once()

    @parameterized.expand([
        ("create_user_bob_dylan", "bob_dylan", "awesomeBob", None, False),
        ("no_username_given", None, "PassWord", "admin", True),
        ("no_password_given", "boy_dylan", None, None, True),
    ])
    def test_add_user_failure(self, _, username, password, role, error):
        if error:
            with self.assertRaises(SQLAlchemyError):
                self.db.add_user(username, password, role)
        else:
            self.db.add_user(username, password, role)

    @parameterized.expand([
        ("Bob_Dylan", "bob_dylan", {"password": "StrongPwd", "role": "admin"}),
        ("Dev_Success", "dev_success", {"role": "user"}),
    ])
    @patch("app.db.db.DB._session", new_callable=MagicMock)
    def test_update_user(self, _, username: str, update_criteron: dict, mock_session):
        mock_session.commit = MagicMock()
        self.db.update_user(username, **update_criteron)
        mock_session.commit.assert_called_once()
        
    @parameterized.expand([
        ("Bob_Dylan", "bob_dylan", "StrongPwd", "user"),
        ("Dev_Success", "dev_success", "PassWord", "admin")
    ])
    def test_find_user_by(self, _, username, password, role):
        self.db.add_user(username=username, hashed_password=password, role=role)
        user = self.db.find_user_by(username=username)
        self.assertEqual(user.username, username)
