import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.db import EmbeddedSQL
from frontend.pages import login, register, buyer as buyer_main
from frontend.utils import clear_screen

def main():
    db = EmbeddedSQL()
    
    session = {"login": None, "role": None}
    while True:
        clear_screen()
        print("\n")
        if session["login"] is None:
            print("="*30)
            print("Welcome!")
            print("="*30)
            print("1. Login\n2. Register\n3. Exit")
            print("="*30)
            choice = input("Selection an option (1-3): ")
            if choice == "1":
                session = login.render(db)
                print("Login placeholder")
            elif choice == "2":
                register.render(db)
                print("Register placeholder")
            elif choice == "3":
                    print("Exiting")
                    db.cleanup()
                    sys.exit(0)
            else:
                print("Invalid option, please try again.")
                input("Press Enter to continue...")

        elif session["role"] == "Admin":
            print("Admin dashboard placeholder")
            # session = buyer_main.render(db, session)
            if input("Type 'x' to logout: ") == 'x':
                session = {"login": None, "role": None}
        
        elif session["role"] == "Buyer":
            print("User dashboard placeholder")
            session = buyer_main.render(db, session)

        elif session["role"] == "Seller":
            print("Guest dashboard placeholder")
            # session = buyer_main.render(db, session)
            if input("Type 'x' to logout: ") == 'x':
                session = {"login": None, "role": None}

        else:
            print("Unknown role. (should not be seeing this)")
            session = {"login": None, "role": None}
            input("Press Enter to reset...")
            

if __name__ == "__main__":
    main()