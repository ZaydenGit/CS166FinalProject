# def get_active_auctions(db, limit = 10, offset = 0):
#     query = """
#         SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.seller_login
#         FROM auction a
#         JOIN item i ON a.item_id = i.item_id
#         WHERE a.auction_status = 'Active'
#         ORDER BY a.auction_id ASC
#         LIMIT %s OFFSET %s
#     """
#     try:
#         col_names, rows = db.execute_query(query, (limit, offset))
#         return True, (col_names, rows)
#     except Exception as e:
#         return False, f"Error: {e}"
    
# def search_auctions(db, keyword, limit = 10, offset = 0):
#     query = """
#         SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.seller_login
#         FROM auction a
#         JOIN item i ON a.item_id = i.item_id
#         WHERE a.auction_status = 'Active' AND (i.item_name ILIKE %s OR i.description ILIKE %s)
#         ORDER BY a.auction_id ASC
#         LIMIT %s OFFSET %s
#     """
#     search_term = f"%{keyword}%"
#     try:
#         col_names, rows = db.execute_query(query, (search_term, search_term, limit, offset))
#         return True, (col_names, rows)
#     except Exception as e:
#         return False, f"Error: {e}"

def get_auctions(db, keyword = "", limit=10, offset=0, sort_mode='1'):
    order_by = "a.auction_id ASC"
    if sort_mode == '2':
        order_by = "a.current_highest_bid ASC"
    elif sort_mode == '3':
        order_by = "a.current_highest_bid DESC"
    elif sort_mode == '4':
        order_by = "i.item_name ASC"
    
    search_term = f"%{keyword}%"
    query = f"""
        SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.seller_login
        FROM auction a
        JOIN item i ON a.item_id = i.item_id
        WHERE a.auction_status = 'Active' AND (i.item_name ILIKE %s OR i.category ILIKE %s)
        ORDER BY {order_by}
        LIMIT %s OFFSET %s
    """
    try:
        col_names, rows = db.execute_query(query, (search_term, search_term, limit, offset))
        return True, (col_names, rows)
    except Exception as e:
        return False, f"Error: {e}"

def get_auction_details(db, auction_id):
    query = """
        SELECT a.auction_id, i.item_name, i.description, i.item_condition, a.current_highest_bid, a.auction_status, a.seller_login
        FROM auction a
        JOIN item i ON a.item_id = i.item_id
        WHERE a.auction_id = %s
    """
    try:
        col_names, rows = db.execute_query(query, (auction_id,))
        if rows:
            return True, rows[0]
    except Exception as e:
        return False, f"Error: {e}"
    
def place_bid(db, auction_id, buyer_login, bid_amount):
    success, details = get_auction_details(db, auction_id)
    if not success:
        return False, "Auction doesn't exist"
    highest_bid = float(details[4])
    status = details[5]
    seller = details[6]

    if status != "Active":
        return False, "Auction is closed already"
    if buyer_login == seller:
        return False, "You cannot bid on your own auction"
    if bid_amount <= highest_bid:
        return False, f"Your bid amount must be higher than the current highest bid (${highest_bid:.2f})"
    
    try:
        _, id_rows = db.execute_query("SELECT COALESCE(MAX(bid_id), 0) + 1 FROM bid;")
        new_bid_id = id_rows[0][0]
        insert_query = """
            INSERT INTO bid (bid_id, auction_id, buyer_login, bid_amount, bid_timestamp)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
        """

        db.execute_update(insert_query, (new_bid_id, auction_id, buyer_login, bid_amount))

        update_query = """
            UPDATE auction
            SET current_highest_bid = %s
            WHERE auction_id = %s;
        """
        db.execute_update(update_query, (bid_amount, auction_id))

        return True, "Bid placed succesfully."
    except Exception as e:
        return False, f"Error placing bid: {e}"

def get_recent_bids(db, auction_id, limit=5):
    query = """
        SELECT buyer_login, bid_amount, bid_timestamp
        FROM bid
        WHERE auction_id = %s
        ORDER BY bid_timestamp DESC
        LIMIT %s;"""
    try:
        col_names, rows = db.execute_query(query, (auction_id, limit))
        return True, rows
    except Exception as e:
        return False, f"Error: {e}"

def get_user_auctions(db, buyer_login):
    query = """ 
        SELECT a.auction_id, i.item_name, MAX(b.bid_amount) as your_bid, a.current_highest_bid
        FROM auction a
        JOIN item i ON a.item_id = i.item_id
        JOIN bid b ON a.auction_id = b.auction_id
        WHERE a.auction_status = 'Active' AND b.buyer_login = %s
        GROUP BY a.auction_id, i.item_name, a.current_highest_bid
        ORDER BY a.auction_id ASC;
    """
    try:
        col_names, rows = db.execute_query(query, (buyer_login,))
        return True, rows
    except Exception as e:
        return False, f"Error: {e}"
    
def update_profile(db, login, password, phone, address, category):
    query = """
        UPDATE users
        SET password = %s, phone_num = %s, address = %s, favorite_category = %s
        WHERE login = %s;
    """
    try:

        db.execute_update(query, (password, phone, address, category if category else None, login))
        return True, "Profile updated successfully."
    except Exception as e:
        return False, f"Error updating profile: {e}"
    
def get_user_details(db, login):
    query = """
        SELECT password, phone_num, address, favorite_category
        FROM users
        WHERE login = %s;
    """
    try:
        col_names, rows = db.execute_query(query, (login,))
        if rows:
            return True, rows[0]
        else:
            return False, "User not found."
    except Exception as e:
        return False, f"Error: {e}"