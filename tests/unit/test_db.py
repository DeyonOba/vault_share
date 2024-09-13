"""
Test database interactions using the DB class.
"""
import unittest
from unittest.mock import patch, MagicMock
from app.db.models import User
from app.db.db import DB


class TestDBModule(unittest.TestCase):
    """Test DB class."""
    def setUp(self):
        """Set up a DB instance with a mock database URL."""
        self.db = DB(database_url="sqlite:///:memory:", echo=False)
        
    @patch("app.db.db.DB._session", new_callable=MagicMock)
    def test_add_user_success(self, mock_session):
        """Test if user is added to database."""
        # Mock the add and commit behavior
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        
        
        user = self.db.add_user("bob_dylan", "awesomeBob")
        
        # Assert that a User object was returned
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "bob_dylan")
        
        # Assert that the session's add and commit methods were called
        mock_session.add.assert_called_once_with(user)
        mock_session.commit.assert_called_once()
