from frontend.utils import clear_screen
from backend.controllers import admin as admin_controller
from backend.controllers import buyer as buyer_controller

def render(db, session):
    while True:
        clear_screen()
        print('--- Admin Dashboard ---')
        print('='*50)
        print("1. Manage users")
        print("2. View & Remove auctions")
        print("3. Logout")
        choice = input("Select an option: ").strip()

        if choice == '1':
            limit = 10
            offset = 0
            while True:
                clear_screen()
                print (f"--- User Directory - Page {offset//limit + 1} ---")
                success, rows = admin_controller.get_all_users(db, limit, offset)
                if success and rows:
                    print(f"{'Username':<25} | {'Role':<10} | {'Phone #':<15} | {'Address'}")
                    print("-" * 75)   
                    for row in rows:
                        login = str(row[0])[:24]
                        role = str(row[1])[:9]
                        phone = str(row[2])[:14]
                        address = str(row[3])[:20]
                        print(f"{login:<25} | {role:<10} | {phone:<15} | {address}")
                elif not rows and not rows and offset > 0:
                    print("No more users to display. Returning to last page")
                    offset -= limit
                    input("Press Enter to go back...")
                    continue
                else:
                    print ("No users found")
                    input("Press Enter to go back...")
                    break
                
                print("-" * 75)  
                print("n. Next page | p. Previous page | b. Back to menu | [edit]. Edit user role")
                nav_choice = input("Select option: ").strip().lower()
                if nav_choice == "n":
                    offset += limit
                elif nav_choice == "p":
                    if offset >= limit:
                        offset -= limit
                    else:
                        print("You are already on the first page.")
                        input("Press Enter to continue...")
                elif nav_choice == "b":
                    break
                elif (nav_choice == "edit"):
                    target = input('Enter username to update: ').strip()
                    print("Available roles: Buyer, Seller, Admin")
                    new_role = input(f"Enter a new role for {target}: ").strip().capitalize()

                    update_success, update_msg = admin_controller.update_user_role(db, target, new_role)
                    print(f"\n[{'Success' if update_success else 'Failed'}] {update_msg}")
                    input("Press Enter to continue.")
                else:
                    print("Invalid option, please try again.")
                    input("Press Enter to continue...")


        elif choice == "2":
            limit = 10
            offset = 0
            keyword = input("Enter category/item to search (press Enter to view all): ")

            while True:
                clear_screen()
                print(f"--- Auction moderation page - Page {offset//limit + 1} ---")
                success, result = buyer_controller.get_auctions(db, keyword, limit, offset, sort_mode='1')

                if success:
                    col_names, rows = result

                    if not rows and offset > 0:
                        print("No more auctions to display. Returning to last page")
                        offset -= limit
                        input("Press Enter to go back...")
                        continue
                    elif not rows and offset == 0:
                        print ("There are no active auctions that match that criteria.")
                        input("Press Enter to go back...")
                        break

                    print(f"{'ID':<5} | {'Item Name':<25} | {'Category':<15} | {'Current Bid':<11} | {'Seller'}")
                    print("-" * 75)

                    for row in rows:
                        a_id = str(row[0])
                        item_name = str(row[1])[:24]
                        category = str(row[2])[:14]
                        current_bid = f"${row[3]:.2f}"
                        seller = str(row[4])[:14]

                        print(f"{a_id:<5} | {item_name:<25} | {category:<15} | {current_bid:<11} | {seller}")
                else:
                    print(f"Error fetching auctions: {result}")
                    break

                print("-" * 75)
                print("n. Next page | p. Previous page | b. Back to menu | [auction ID]. Delete auction")
                nav_choice = input("Select option: ").strip().lower()

                if nav_choice == "n":
                    offset += limit
                elif nav_choice == "p":
                    if offset >= limit:
                        offset -= limit
                    else:
                        print("You are already on the first page.")
                        input("Press Enter to continue...")
                elif nav_choice == 'b': break
                elif nav_choice.isdigit():
                    print("\n*** WARNING: THIS CANNOT BE UNDONE ***")
                    confirm = input(f"Permanently delete Auction #{nav_choice} and its item? (y/n): ").strip().lower()
                    if confirm == 'y':
                        delete_success, delete_msg = admin_controller.delete_auction_and_item(db, nav_choice)
                        print(f"\n[{'Success' if delete_success else 'Failed'}] {delete_msg}")
                    input("Press Enter to continue...")
                else:
                    print("\nInvalid option.")
                    input("Press Enter to continue...")