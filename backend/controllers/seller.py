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
    try:
        bid_query = """
            SELECT buyer_login, bid_amount
            FROM bid
            WHERE auction_id = %s
            ORDER BY bid_amount DESC LIMIT 1;
        """
        _, bid_rows = db.execute_query(bid_query, (auction_id,))
        if bid_rows:
            winner_login = str(bid_rows[0][0])
            winning_bid = float(bid_rows[0][1])

            update_auction = """
                UPDATE auction
                SET auction_status = 'Closed', winner_login = %s, winner_role = 'Buyer'
                WHERE auction_id = %s AND seller_login = %s AND auction_status = 'Active';
            """
            db.execute_update(update_auction, (winner_login, auction_id, seller_login))

            _, pay_id_rows = db.execute_query("SELECT COALESCE(MAX(payment_id), 0) + 1 FROM payment;")
            payment_id = int(pay_id_rows[0][0])

            pay_query = """
                INSERT INTO payment (payment_id, auction_id, buyer_login, amount, payment_status)
                VALUES (%s, %s, %s, %s, 'Pending');
            """
            db.execute_update(pay_query, (payment_id, auction_id, winner_login, winning_bid))
            return True, f"Auction closed - won by {winner_login} with a bid of ${winning_bid:.2f}"
        else:
            update_auction = """
                UPDATE auction
                SET auction_status = 'Closed'
                WHERE auction_id = %s AND seller_login = %s AND auction_status = 'Active';
            """
            db.execute_update(update_auction, (auction_id, seller_login))
            return True, f"Auction ${auction_id} closed with no bids"
    except Exception as e:
        db._connection.rollback()
        return False, f"Error: {e}"
    
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
    
def get_pending_shipments(db, seller_login):
    query = """
        SELECT s.shipment_id, i.item_name, s.address, s.shipment_status, s.tracking_number
        FROM shipment s
        JOIN auction a ON s.auction_id = a.auction_id
        JOIN item i ON a.item_id = i.item_id
        WHERE a.seller_login = %s AND s.shipment_status != 'Delivered';
    """
    try:
        _, rows = db.execute_query(query, (seller_login,))
        return True, rows
    except Exception as e:
        return False, f"{e}"
    
def update_shipment(db, shipment_id, seller_login, new_status, tracking_num=None):
    query = """
        UPDATE shipment
        SET shipment_status = %s, tracking_number = COALESCE(%s, tracking_number)
        FROM auction
        WHERE shipment.auction_id = auction.auction_id
            AND shipment.shipment_id = %s 
            AND auction.seller_login = %s;
    """
    try:
        db.execute_update(query, (new_status, tracking_num, shipment_id, seller_login))
        return True, "Shipment updated."
    except Exception as e:
        db._connection.rollback()
        return False, f"Failed to update shipment: {e}"