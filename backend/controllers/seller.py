def create_auction (db, seller_login, name, description, condition, category, start_price):
    try:
        description_val = description if description else None
        _, item_rows = db.execute_query("SELECT COALESCE(MAX(item_id), 0) + 1 FROM item;")
        item_id = item_rows[0][0]
        item_query = """
            INSERT INTO item (item_id, item_name, description, item_condition, category, starting_price, seller_login)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        db.execute_update(item_query, (item_id, name, description_val, condition, category, start_price, seller_login))

        _, auction_rows = db.execute_query("SELECT COALESCE(MAX(auction_id), 0) + 1 FROM auction;")
        auction_id = auction_rows[0][0]
        auction_query = """
            INSERT INTO auction (auction_id, item_id, seller_login, current_highest_bid, auction_status)
            VALUES (%s, %s, %s, %s, 'Active');
        """
        db.execute_update(auction_query, (auction_id, item_id, seller_login, start_price))
        return True, f"Auction created with ID {auction_id}"
    except Exception as e:  
        return False, f"Error in creating item: {e}"
    
def get_seller_auctions(db, seller_login, status="Active"):
    query = """
        SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid
        FROM auction a
        JOIN item i ON a.item_id = i.item_id
        WHERE a.seller_login = %s and a.auction_status = %s
        ORDER by a.auction_id ASC;"""
    
    try:
        col_names, rows = db.execute_query(query, (seller_login, status))
        return True, rows
    except Exception as e:
        return False, f"DB error: {e}"

def end_auction(db, auction_id, seller_login):
    query = """
        UPDATE auction
        SET auction_status = 'Closed'
        WHERE auction_id = %s AND seller_login = %s AND auction_status = 'Active';
    """
    try:
        db.execute_update(query, (auction_id, seller_login))
        return True, f"Auction ${auction_id} closed"
    except Exception as e:
        return False, f"DB error: {e}"
    
def update_description(db, auction_id, seller_login, new_description):
    query = """
        UPDATE item
        SET description = %s
        FROM auction
        WHERE item.item_id = auction.item_id AND auction.auction_id = %s AND auction.seller_login = %s AND auction.auction_status = 'Active';
    """
    try:
        description_val = new_description if new_description else None
        db.execute_update(query, (description_val, auction_id, seller_login))
        return True, 'Successfully updated description'
    except Exception as e:
        db._connection.rollback()
        return False, f"Failed to update description: {e}"