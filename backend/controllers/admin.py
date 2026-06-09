def get_all_users(db, limit=10, offset=0):
    query = """
        SELECT login, role, phone_num, address
        FROM users
        ORDER BY login ASC
        LIMIT %s OFFSET %s;
    """
    try:
        col_names, rows = db.execute_query(query, (limit, offset))
        return True, rows
    except Exception as e:
        return False, f"Error: {e}"
    
def update_user_role(db, user_login, new_role):
    roles = ['Buyer', 'Seller', 'Admin']
    if new_role not in roles:
        return False, f"Invalid role. Enter one of {','.join(roles)}"
    query = "UPDATE users SET role = %s WHERE login = %s"
    try:
        db.execute_update(query, (new_role, user_login))
        return True, f"User {user_login} was updated to {new_role}"
    except Exception as e:
        db._connection.rollback()
        if "auction_winner_role_check" in str(e).lower():
            return False, f"Cannot promote {user_login} because they have already won an auction (restricted to Buyer)."
        elif "bid_buyer_role_check" in str(e).lower() or "bid_buyer_login_fkew" in str(e).lower():
            return False, f"Cannot change role, {user_login} has an active or past bid (restricted to Buyer)"
        return False, f"Failed to update role: {e}"

def delete_auction_and_item(db, auction_id):
    try:
        _, item_rows = db.execute_query("SELECT item_id FROM auction WHERE auction_id = %s", (auction_id,))
        if not item_rows:
            return False, "Auction ID not found"
        item_id = item_rows[0][0]

        db.execute_update("DELETE FROM bid WHERE auction_id = %s", (auction_id,))
        db.execute_update("DELETE FROM auction WHERE auction_id = %s", (auction_id,))
        db.execute_update("DELETE FROM item WHERE item_id = %s", (item_id,))

        return True, f"Successfully deleted auction #{auction_id} and associated tuples"
    except Exception as e:
        db._connection.rollback()
        return False, f"Error: {e}"

