import allure
import pytest
import psycopg2
from database.queries import create_user, get_user_by_email, delete_user_by_email, count_users, update_user_age


@allure.feature("Database")
@allure.title("Создание пользователя")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user(db, cleanup_user):
    create_user(db, "Test", cleanup_user, 99)
    user = get_user_by_email(db, cleanup_user)
    assert user is not None


@allure.feature("Database")
@allure.title("Удаление пользователя")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_user(db, unique_email):
    create_user(db, "Test", unique_email, 99)
    delete_user_by_email(db, unique_email)
    user = get_user_by_email(db, unique_email)
    assert user is None


@allure.feature("Database")
@allure.title("Неизвестный пользователь")
@allure.severity(allure.severity_level.MINOR)
def test_user_not_found(db):
    user = get_user_by_email(db, "nonexistent_xyz@test.com")
    assert user is None


@allure.feature("Database")
@allure.title("Создание дубликата email")
@allure.severity(allure.severity_level.NORMAL)
def test_duplicate_email_raises(db, cleanup_user):
    create_user(db, "Test", cleanup_user, 99)
    with pytest.raises(psycopg2.errors.UniqueViolation):
        create_user(db, "Test", cleanup_user, 99)


@allure.feature("Database")
@allure.title("Увеличение счетчика")
@allure.severity(allure.severity_level.MINOR)
def test_count_increases(db, cleanup_user):
    before = count_users(db)
    create_user(db, "Test", cleanup_user, 25)
    after = count_users(db)
    assert after == before + 1


def test_update_user(db, cleanup_user):
    user = create_user(db, "Test", cleanup_user, 99)
    new_age = update_user_age(db, cleanup_user, 25)
    assert user[3] == new_age

def test_get_adults(db, unique_email):
    create_user(db, "Test", unique_email, 25)
    create_user(db, "Test", unique_email, 17)
    rows = db.fetch_all("SELECT * FROM users WHERE age >= %s AND email LIKE %s", (18, "test_%"))
    assert rows[3] >= 18

def test_order_by_age(db, cleanup_user):
    rows = db.fetch_all("SELECT * FROM users WHERE email LIKE %s ORDER BY age ASC", ("test_%",))
    assert rows[0][3] <= rows[1][3]