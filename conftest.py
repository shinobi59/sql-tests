import pytest
from database.connection import Database
import time


@pytest.fixture(scope="session")
def db():
    database = Database(
        host="localhost",
        port=5432,
        database="qa_learning",
        user="postgres",
        password="postgres"
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