import os
from backend import auth
from frontend.utils import clear_screen

def render(db):
    clear_screen()
    print("User registration")

    while True:
        username = input("Enter username: ").strip()
        if username: break
        print("Username cannot be empty.")

    while True:
        password = input("Enter password: ").strip()
        if password: break
        print("Password cannot be empty.")

    while True:
        phone = input("Enter phone number: ").strip()
        if phone: break
        print("Phone number cannot be empty.")

    while True:
        address = input("Enter address: ").strip()
        if address: break
        print("Address cannot be empty.")

    fav_category = input("Enter favorite category (optional): ").strip()

    sucess, message = auth.register_user(db, username, password, phone, address, fav_category)

    if sucess: print(f"\nSuccess: User '{username}' registered successfully.")
    else: print(f"\nError: {message}")