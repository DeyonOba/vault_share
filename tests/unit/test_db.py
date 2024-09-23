"""
Test database interactions using the DB class.
"""
import unittest
from unittest.mock import patch, MagicMock
from vaultShare.db.models import User
from vaultShare.db import DB
from parameterized import parameterized
from sqlalchemy.exc import SQLAlchemyError

class TestDBModule(unittest.TestCase):
    """Test DB class."""
    def setUp(self):
        """Set up a DB instance with a mock database URL."""
        self.db = DB(database_url="sqlite:///:memory:", echo=False)
    
    @parameterized.expand([
        ("Bob_Dylan", "bob_dylan", "awesomeBob", "user"),
        ("John_Doe", "john_doe", "justGiveMeAcess", "user"),
        ("Dev_Success", "dev_success", "PassWord", "admin"),
    ])   
    @patch("vaultShare.db.DB._session", new_callable=MagicMock)
    def test_add_user_success(self, _, username, password, role, mock_session):
        """Test if user is added to database."""
        # Mock the add and commit behavior
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        
        user = self.db.create(
            User, username=username, 
            hashed_password=password, role=role
        )

        # Assert that a User object was returned
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, username)
        self.assertEqual(user.hashed_password, password)
        self.assertEqual(user.role, role)
        
        # Assert that the session's add and commit methods were called
        mock_session.add.assert_called_once_with(user)
        mock_session.commit.assert_called_once()
