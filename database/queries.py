def safe_execute(db, query, params=None):
    try:
        db.execute(query, params)
        db.commit()
    except Exception:
        db.rollback()
        raise


def create_user(db, name, email, age):
    safe_execute(
        db,
            "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
            (name, email, age),
        )


def get_user_by_email(db, email):
    return db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))

def delete_user_by_email(db, email):
    safe_execute(
        db,
        ("DELETE FROM users WHERE email = %s",
        (email,))
    )


def count_users(db):
    row = db.fetch_one("SELECT COUNT(*) FROM users")
    return row[0]

def update_user_age(db, email, new_age):
    safe_execute(
        db,
        "UPDATE users SET age = %s WHERE email = %s", (new_age, email),
    )