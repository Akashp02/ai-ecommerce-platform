from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.test_config import TEST_DATABASE_URL


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)