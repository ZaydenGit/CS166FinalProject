from frontend.utils import clear_screen
from backend.controllers import seller as seller_controller

def render(db, session):
    while True:
        clear_screen()
        print('--- Seller dashboard ---')

        print("=================================")
        print("1. List an item")
        print("2. Manage active auctions")
        print("3. View closed auctions")
        print("x. Logout")
        print("=================================")

        choice = input("Select an option: ").strip().lower()

        if choice == '1':
            clear_screen()
            while True:
                name = input("Item name:" ).strip()
                if name: break
                print("Name must not be empty")
            desc = input("Description: ").strip()
            condition = input("Condition (e.g. New, Used, Refurbished, Parts): ").strip()
            category = input("Category: ").strip()

            while True:
                price_str = input("Starting Price: $").strip()
                try:
                    price = float(price_str)
                    if price >= 0: break
                    print("Price must be 0 or higher")
                except ValueError:
                    print("Invalid amount. Enter a nuber")
            success, msg = seller_controller.create_auction(db, session["login"], name, desc, condition, category, price)
            print(f"{'Successfully created item' if success else 'Failed to create item'} {msg}")
            input("Press enter to continue")
            

        elif choice == '2':
            while True:
                clear_screen()
                print ("--- Active auctions ---")
                success, rows = seller_controller.get_seller_auctions(db, session["login"], 'Active')

                if success and rows:
                    print(f"{'ID':<5} | {'Item Name':<25} | {'Highest Bid'}")
                    print('-'*50)
                    for row in rows:
                        a_id = row[0]
                    name = row[1]
                    highest_bid = float(row[3]) if row[3] is not None else 0.0
                    print(f"{str(a_id):<5} | {str(name)[:24]:<25} | ${highest_bid:.2f}")
                elif success and not rows:
                    print("You do not have any auctions")
                else:
                    print(f"Error: {rows}")
                print('-'*50)
                print('[auction ID] Type an auction ID to manage it | [b] Go back')
                action = input("Select option: ").strip().lower()

                if action == 'b': break
                elif action.isdigit():
                    print(f"1. Close auction\n2. Edit description\nb. Cancel")
                    sub_action = input("Selection option: ").strip()
                    if sub_action == '1':
                        confirm = input(f"Are you sure you want to close ${action}? (y/n): ").strip().lower()
                        if confirm == 'y':
                            close_success, close_msg = seller_controller.end_auction(db, action, session["login"])
                            print(f"{'Successfully closed auction' if close_success else 'Failed to close auction'} {close_msg}")
                            input("Press Enter to continue...")
                    elif sub_action == '2':
                        new_description = input("Enter new description (leave blank to clear): ")
                        update_success, update_msg = seller_controller.update_description(db, action, session["login"], new_description)
                        print(f"{'Successfully updated item' if update_success else 'Failed to update item'} {update_msg}")
                        input("Press enter to continue.")
                else:
                    print("Invalid option.")
                    input("Press Enter to continue")

        elif choice == '3':
            clear_screen()
            print('--- Closed Auctions ---')
            success, rows = seller_controller.get_seller_auctions(db, session["login"], 'Closed')
            if success and rows:
                print(f"{'ID':<5} | {'Item Name':<25} | {'Final Bid'}")
                print('-'*50)
                for row in rows:
                    a_id = row[0]
                    name = row[1]
                    final_bid = float(row[3]) if row[3] is not None else 0.0
                    print(f"{str(a_id):<5} | {str(name)[:24]:<25} | ${final_bid:.2f}")
                input("Press Enter to continue...")
            elif success and not rows:
                print("You have no closed auctions")
                input("Press Enter to continue...")
            else:
                print(f"Error: {rows}")

        elif choice == "x":
            print("Logging out...")
            return {"login": None, "role": None}

        else: 
            print("Invalid option, please try again.")
            input("Press Enter to continue...")