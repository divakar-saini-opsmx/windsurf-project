import json
import base64
import os

class PasswordManager:
    def __init__(self, filename='passwords.json'):
        self.filename = filename
        self.passwords = self.load_passwords()

    def load_passwords(self):
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return {}
        with open(self.filename, 'r') as f:
            return json.load(f)


    def save_passwords(self):
        with open(self.filename, 'w') as f:
            json.dump(self.passwords, f)

    def add_password(self, website, account, password):
        encoded_password = base64.b64encode(password.encode()).decode()
        self.passwords[website] = {'account': account, 'password': encoded_password}
        self.save_passwords()

    def retrieve_password(self, website):
        if website in self.passwords:
            encoded_password = self.passwords[website]['password']
            return base64.b64decode(encoded_password).decode()
        else:
            return None

def main():
    pm = PasswordManager()
    while True:
        print("1. Add password")
        print("2. Retrieve password")
        print("3. Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            website = input("Enter website: ")
            account = input("Enter account: ")
            password = input("Enter password: ")
            pm.add_password(website, account, password)
        elif choice == "2":
            website = input("Enter website: ")
            password = pm.retrieve_password(website)
            if password:
                print("Password:", password)
            else:
                print("No password found for that website.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
