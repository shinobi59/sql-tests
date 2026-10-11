import pytest
from database.connection import Database
import time
import os



@pytest.fixture(scope="session")
def db():
    database = Database(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "qa_learning"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )
    yield database
    database.close()

@pytest.fixture
def unique_email():
    return f"test_{int(time.time() * 1000)}@test.com"

@pytest.fixture
def cleanup_user(db, unique_email):
    yield unique_email
    db.execute("DELETE FROM users WHERE email = %s", (unique_email,))
    db.commit()

@pytest.fixture
def cleanup_emails(db, unique_email):
    emails = [unique_email, f"{unique_email}_2"]
    yield emails
    db.execute("DELETE FROM users WHERE email = ANY(%s)", (emails,))
    db.commit()