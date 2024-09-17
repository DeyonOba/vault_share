"""
Test Authentication modules.
"""
import unittest
from parameterized import parameterized
from app.auth.auth_utils import _hash_password, verify_password


class TestAuthUtils(unittest.TestCase):
    """
    Test Authentication utils modules.
    """
    @parameterized.expand([
        ("short_password", "OnE"),
        ("with_special_characters", "@validPassword&"),
        ("with_numbers", "1BeautifulPassword"),
        ("with_white_space", "My  Password$Code")
    ])
    def test_verify_password_success(self, _, password):
        """Test verifies valid passwords."""
        hashed_password = _hash_password(password)
        self.assertTrue(verify_password(password, hashed_password))
    
    @parameterized.expand([
        ("missing_uppercase", "onE", "OnE"),
        ("wrong_special_character", "@validPassword!", "@validPassword&"),
        ("wrong_number_added", "2BeautifulPassword", "1BeautifulPassword"),
        ("missing_a_white_space", "My Password$Code", "My  Password$Code"),
    ])
    def test_verify_password_failure(self, _, wrong_password, password):
        """Test rejects invalid passwords."""
        hashed_password = _hash_password(password)
        self.assertFalse(verify_password(wrong_password, hashed_password))
