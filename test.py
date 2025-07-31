import unittest
from password_manager import PasswordManager
import json

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.pm = PasswordManager('test_passwords.json')

    def test_add_password(self):
        self.pm.add_password('example.com', 'user', 'password123')
        self.assertIn('example.com', self.pm.passwords)
        self.assertEqual(self.pm.passwords['example.com']['account'], 'user')
        self.assertEqual(self.pm.passwords['example.com']['password'], 'cGFzc3dvcmQxMjM=')

    def test_retrieve_password(self):
        self.pm.add_password('example.com', 'user', 'password123')
        self.assertEqual(self.pm.retrieve_password('example.com'), 'password123')
        self.assertIsNone(self.pm.retrieve_password('nonexistent.com'))

    def test_load_passwords(self):
        self.pm.add_password('example.com', 'user', 'password123')
        self.pm.save_passwords()
        new_pm = PasswordManager('test_passwords.json')
        self.assertIn('example.com', new_pm.passwords)

    def test_save_passwords(self):
        
        self.pm.add_password('example.com', 'user', 'password123')
        self.pm.save_passwords()
        with open('test_passwords.json', 'r') as f:
            self.assertEqual(json.load(f), self.pm.passwords)

if __name__ == "__main__":
    unittest.main()