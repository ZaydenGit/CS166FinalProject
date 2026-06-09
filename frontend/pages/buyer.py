from frontend.utils import clear_screen
from backend.controllers import buyer as buyer_controller
from backend import auth

def view_auction_page(db, session, auction_id):
    while True:
        clear_screen()
        success,details = buyer_controller.get_auction_details(db, auction_id)
        if not success:
            print(f"Error: {details}")
            input("Press Enter to go back...")
            return
        a_id, name, desc, cond, highest_bid, status, seller = details

        print("--- Auction Details ---")
        print("="*50)
        print(f"Name: {name}")
        print(f"Condition: {cond}")
        print(f"Status: {status}")
        print(f"Seller: {seller}")
        print(f"\nDescription: {desc}")
        print(f"\nCurrent highest bid: ${highest_bid:.2f}")
        print("="*50)

        if status == "Active":
            print("1. Place a bid")
            print("2. View recent bids")
            print("b. Go back to menu")

        choice = input("Select an option: ").strip().lower()
        if choice == "1" and status == "Active":
            bid_input = input(f"Enter bid amount (current highest bid: ${highest_bid:.2f}): $").strip()
            try:
                bid_amount = float(bid_input)
                bid_success, msg = buyer_controller.place_bid(db, auction_id, session["login"], bid_amount)
                if bid_success: print(f"Success: {msg}")
                else: print(f"Failed to place bid: {msg}")
            except ValueError:
                print("Invalid bid amount. Please enter a valid number.")
            input("Press Enter to continue...")
        elif choice == "2":
            success_bids, recent_bids = buyer_controller.get_recent_bids(db, auction_id)
            if success_bids and recent_bids:
                print("\nRecent Bids:")
                print(f"{'Bidder':<15} | {'Amount':<10} | {'Time'}")
                print("-" * 50)
                for bidder, amount, timestamp in recent_bids:
                    print(f"{bidder:<15} | ${amount:<9.2f} | {timestamp}")
            else:
                print("No bids placed yet")
            input("Press Enter to continue...")
            continue
        elif choice == "b": return
        else:
            print("Invalid option")
            input("Press Enter to continue...")

def browse_auctions_page(db, session):
    clear_screen()
    keyword = input("Enter category or item name to search (or press Enter to view all): ").strip()

    print("\nSort all active auctions by:")
    print("1. Auction ID (default)")
    print("2. Price (Low to High)")
    print("3. Price (High to Low)")
    print("4. Item Name")
    sort_choice = input("Select sorting option (1-4): ").strip()
    if sort_choice not in ['1', '2', '3', '4']:
        sort_choice = '1'

    limit = 10
    offset = 0
    
    while True:
        clear_screen()
        print (f"--- Search results for {keyword} - Page {offset//limit + 1} ---" if keyword else f"--- Active auctions - Page {offset//limit + 1} ---")
        success, result = buyer_controller.get_auctions(db, keyword, limit, offset, sort_choice)
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
        print("n. Next page | p. Previous page | b. Back to menu | [auction ID]. View auction details")
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
        elif (nav_choice.isdigit()):
            view_auction_page(db, session, nav_choice)
        else:
            print("Invalid option, please try again.")
            input("Press Enter to continue...")



def render(db, session):
    while True:
        clear_screen()
        print("--- Buyer dashboard ---")
        
        success, my_auctions = buyer_controller.get_user_auctions(db, session["login"])
        if success and my_auctions:
            print("\nYour Bids:")
            print(f"{'ID':<5} | {'Item Name':<20} | {'Your Bid':<10} | {'Highest Bid'}")
            print("-" * 70)
            
            for a_id, item_name, your_bid, current_bid in my_auctions:
                status_mark = "*" if your_bid == current_bid else ""
                print(f"{str(a_id):<5} | {item_name[:19]:<20} | ${your_bid:<9.2f} | ${current_bid:.2f} {status_mark}")
            print("\n(* indicates that you are the highest bidder)")
        else:
            print("\nYou have not placed any bids yet.")
        
        print("=================================")
        print("1. View all or search active auctions")
        print("2. View auction by ID")
        print("3. Edit profile")
        print("x. Logout")
        print("=================================")

        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            browse_auctions_page(db, session)
            
        elif choice == "2":
            a_id = input("Enter auction id: ").strip()
            if a_id.isdigit():
                view_auction_page(db, session, a_id)
            else:
                print("Auction id should be a number")
                input('Press Enter to continue...')

        elif choice == "3":
            print("-- Edit Profile -- \n")
            current_password = input("Enter current password: ").strip()

            is_valid, _ = auth.login_user(db, session["login"], current_password)
            if not is_valid:
                print("Incorrect password. Returning to menu.")
                input("Press Enter to continue...")
                continue

            success, profile = buyer_controller.get_user_details(db, session["login"])
            if not success:
                print(f"Error fetching profile: {profile}")
                input("Press Enter to continue...")
                continue

            current_password, current_phone, current_address, current_category = profile
            current_category = current_category if current_category else "None"

            print('-'*40)
            print("Leave a field empty and press Enter to keep current value.")
            new_password = input("Enter new password: ").strip()
            new_phone = input(f"Enter new phone number ({current_phone}): ").strip()
            new_address = input(f"Enter new address ({current_address}): ").strip()
            new_category = input(f"Enter new favorite category ({current_category}): ").strip()

            update_success, msg = buyer_controller.update_profile(db,
                session["login"],
                new_password if new_password else current_password,
                new_phone if new_phone else current_phone,
                new_address if new_address else current_address,
                new_category if new_category else current_category
            )
            print(f"Successfully updated proifle" if update_success else f"Failed to update profile: {msg}")
            input("Press Enter to continue...")
            
        elif choice == "x":
            print("Logging out...")
            return {"login": None, "role": None}
        
        else:
            print("Invalid option, please try again.")
            input("Press Enter to continue...")