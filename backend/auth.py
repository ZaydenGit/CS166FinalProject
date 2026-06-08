import psycopg2

def register_user(db, login, password, phone, address, fav_category):
    query = """
        INSERT INTO users (login, password, phone_num, address, role, favorite_category)
        VALUES (%s, %s, %s, %s, 'Buyer', %s)
    """

    category = fav_category if fav_category else None
    params = (login, password, phone, address, category)

    try:
        db.execute_update(query, params)
        return True, "Successful registration."
    except psycopg2.IntegrityError as e:
        db._connection.rollback()
        if "unique constraint" in str(e).lower() or "users_pkey" in str(e).lower():
            return False, "User already exists. Please try again."
        return False, f"DB error: {e}"
    except Exception as e:
        db._connection.rollback()
        return False, f"Unexpected error: {e}"
    
def login_user(db, login, password):
    query = """
        SELECT role FROM users WHERE login = %s AND password = %s
    """
    try:
        col_names, rows = db.execute_query(query, (login, password))
        if rows:
            return True, rows[0][0]
        else:
            return False, "Invalid login or password. Please try again."
    except Exception as e:
        db._connection.rollback()
        return False, f"Unexpected error: {e}"