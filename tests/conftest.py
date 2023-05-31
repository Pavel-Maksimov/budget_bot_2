import pytest
import pytest_asyncio

from budget_bot_2.models import Base
from tests.factories import OutcomeCategoryFactory
from tests.testing_db_connection import TestSession, sync_engine


@pytest.fixture(name="db", scope="package", autouse=True)
def create_tables():
    Base.metadata.create_all(sync_engine)
    yield
    Base.metadata.drop_all(sync_engine)


@pytest_asyncio.fixture(name="test_session")
async def create_test_session():
    session = TestSession()
    yield session
    await session.close()


@pytest_asyncio.fixture()
async def add_category(test_session: TestSession):
    added_categories = []

    async def _add_category():
        category = OutcomeCategoryFactory()
        test_session.add(category)
        await test_session.commit()
        return category

    yield _add_category

    for category in added_categories:
        test_session.delete(category)
