import unittest

from app.models import User



class UserModelTestCase(unittest.TestCase):

    def test_password_setter(self):
        u = User(password='abcdefg')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='abcdefg')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='abcdefg')
        self.assertTrue(u.verify_password('abcdefg'))
        self.assertFalse(u.verify_password('password'))

    def test_password_salts_are_random(self):
        u = User(password='abcdefg')
        u2 = User(password='abcdefg')
        self.assertTrue(u.password_hash != u2.password_hash)