from fastapi.testclient import TestClient
import pytest
from app.main import app

from app.db.base import Base
from app.db.test_session import test_engine
from app.db.test_session import TestingSessionLocal

from app.db.dependencies import get_db
from sqlalchemy import text

# -----------------------------
# Create test tables
# -----------------------------

Base.metadata.create_all(bind=test_engine)


# -----------------------------
# Override DB dependency
# -----------------------------

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# -----------------------------
# Test client
# -----------------------------

@pytest.fixture
def client():
    return TestClient(app)

# -----------------------------
# Cleanup helper
# -----------------------------

def cleanup_tables():

    db = TestingSessionLocal()

    db.execute(text("DELETE FROM product_reviews"))
    db.execute(text("DELETE FROM payments"))
    db.execute(text("DELETE FROM order_items"))
    db.execute(text("DELETE FROM orders"))
    db.execute(text("DELETE FROM addresses"))
    db.execute(text("DELETE FROM products"))
    db.execute(text("DELETE FROM categories"))
    db.execute(text("DELETE FROM users"))

    db.commit()
    db.close()


def pytest_runtest_teardown():

    cleanup_tables()

from app.db.test_session import TestingSessionLocal
from app.models.user import User
from app.core.security import hash_password


def create_admin_user():

    db = TestingSessionLocal()

    admin = User(
        first_name="Admin",
        last_name="Test",
        email="admin@test.com",
        password_hash=hash_password("Password@123"),
        role="admin"
    )

    db.add(admin)
    db.commit()

    db.close()