import hashlib
import os
import json

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = hashlib.sha256(master_password.encode()).hexdigest()
        self.data = {}

    def encrypt(self, data):
        # In a real-world scenario, use a more robust encryption algorithm
        return hashlib.sha256(data.encode()).hexdigest()

    def save_data(self):
        with open('passwords.json', 'w') as f:
            f.write(json.dumps(self.data))

    def load_data(self):
        if os.path.exists('passwords.json'):
            with open('passwords.json', 'r') as f:
                self.data = json.load(f)

    def authenticate(self, master_password):
        return hashlib.sha256(master_password.encode()).hexdigest() == self.master_password

    def add_password(self, website, username, password):
        if not self.authenticate(input("Enter your master password to add a new password: ")):
            print("Authentication failed. Unable to add password.")
            return

        encrypted_password = self.encrypt(password)
        self.data[website] = {
            'username': username,
            'password': encrypted_password
        }
        self.save_data()
        print(f"Password for {website} added successfully.")

    def get_password(self, website):
        if not self.authenticate(input("Enter your master password to retrieve the password: ")):
            print("Authentication failed. Unable to get password.")
            return

        if website in self.data:
            encrypted_password = self.data[website]['password']
            password = self.encrypt(encrypted_password)
            print(f"Password for {website}: {password}")
        else:
            print(f"No password found for {website}.")

if __name__ == "__main__":
    print("Welcome to the Password Manager!")
    master_password = input("Please set your master password: ")

    password_manager = PasswordManager(master_password)
    password_manager.load_data()

    while True:
        print("\nOptions:")
        print("1. Add new password")
        print("2. Get password")
        print("3. Exit")

        choice = int(input("Enter the option number: "))

        if choice == 1:
            website = input("Enter the website: ")
            username = input("Enter your username: ")
            password = input("Enter the password: ")
            password_manager.add_password(website, username, password)
        elif choice == 2:
            website = input("Enter the website: ")
            password_manager.get_password(website)
        elif choice == 3:
            password_manager.save_data()
            print("Password Manager closed.")
            break
        else:
            print("Invalid option. Please try again.")
