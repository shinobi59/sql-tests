def create_user(db, name, email, age):
    try:
        db.execute(
            "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
            (name, email, age),
        )
        db.commit()
    except Exception:
        db.rollback()
        raise   # ← обязательно! Пробрасываем исключение дальше

def get_user_by_email(db, email):
    return db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))

def delete_user_by_email(db, email):
    db.execute("DELETE FROM users WHERE email = %s", (email,))
    db.commit()

def count_users(db):
    row = db.fetch_one("SELECT COUNT(*) FROM users")
    return row[0]