import os
from backend import auth
from frontend.utils import clear_screen

def render(db):
    clear_screen()
    print("User login")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    sucess, message = auth.login_user(db, username, password)

    if sucess:
        print(f"\nLogged in as '{username}' with role '{message}'.")
        return {"login": username, "role": message}
    else:
        print(f"\nError: {message}")
        return {"login": None, "role": None}