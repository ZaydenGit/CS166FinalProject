import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.db import EmbeddedSQL


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    db = EmbeddedSQL()

    while True:
        clear_screen()
        print("1. Login 2. Register 3.Exit")
        choice = input("Selection an option (1-3): ")
        match choice:
            case 1:
                print("Login placeholder")
            case 2:
                print("Register placeholder")   
            case 3:
                print("Exiting")
                db.cleanup()
                sys.exit(0)

if __name__ == "__main__":
    main()