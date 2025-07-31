import unittest
import json
import base64
import tempfile
import os
from password_manager import PasswordManager

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.filename = tempfile.mkstemp()[1]
        self.pm = PasswordManager(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_init(self):
        self.assertEqual(self.pm.filename, self.filename)
        self.assertEqual(self.pm.passwords, {})

    def test_load_passwords(self):
        with open(self.filename, 'w') as f:
            json.dump({'website': {'account': 'account', 'password': 'password'}}, f)
        self.pm = PasswordManager(self.filename)
        self.assertEqual(self.pm.passwords, {'website': {'account': 'account', 'password': 'password'}})

    def test_load_passwords_file_not_found(self):
        self.assertEqual(self.pm.passwords, {})

    def test_save_passwords(self):
        self.pm.passwords = {'website': {'account': 'account', 'password': 'password'}}
        self.pm.save_passwords()
        with open(self.filename, 'r') as f:
            self.assertEqual(json.load(f), {'website': {'account': 'account', 'password': 'password'}})

    def test_add_password(self):
        self.pm.add_password('website', 'account', 'password')
        self.assertEqual(self.pm.passwords, {'website': {'account': 'account', 'password': base64.b64encode('password'.encode()).decode()}})

    def test_retrieve_password(self):
        self.pm.add_password('website', 'account', 'password')
        self.assertEqual(self.pm.retrieve_password('website'), 'password')

    def test_retrieve_password_not_found(self):
        self.assertIsNone(self.pm.retrieve_password('website'))

    def test_add_multiple_passwords(self):
        self.pm.add_password('website1', 'account1', 'password1')
        self.pm.add_password('website2', 'account2', 'password2')
        self.assertEqual(self.pm.passwords, {'website1': {'account': 'account1', 'password': base64.b64encode('password1'.encode()).decode()}, 'website2': {'account': 'account2', 'password': base64.b64encode('password2'.encode()).decode()}})

    def test_retrieve_multiple_passwords(self):
        self.pm.add_password('website1', 'account1', 'password1')
        self.pm.add_password('website2', 'account2', 'password2')
        self.assertEqual(self.pm.retrieve_password('website1'), 'password1')
        self.assertEqual(self.pm.retrieve_password('website2'), 'password2')

if __name__ == "__main__":
    unittest.main()
