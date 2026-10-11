import time
from database.connection import Database


db = Database(
    host="localhost",
    port=5432,
    database="qa_learning",
    user="postgres",
    password="postgres",
)

# 1. Все пользователи — без %s
rows = db.fetch_all("SELECT * FROM users")
print("Все пользователи:", rows)

# 2. Один — есть %s, передаём (1,)
one = db.fetch_one("SELECT * FROM users WHERE id = %s", (1,))
print("Один:", one)

# 3. Уникальный email
email = f"test_{int(time.time())}@test.com"

# 4. Вставить — есть 3 %s, передаём (name, email, age)
db.execute(
    "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
    ("Test", email, 99),
)
db.commit()

# 5. Проверить — есть %s, передаём (email,)
inserted = db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))
print("После вставки:", inserted)

# 6. Удалить — есть %s, передаём (email,)
db.execute("DELETE FROM users WHERE email = %s", (email,))
db.commit()

# 7. Проверить удаление — есть %s, передаём (email,)
after = db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))
print("После удаления:", after)

db.close()