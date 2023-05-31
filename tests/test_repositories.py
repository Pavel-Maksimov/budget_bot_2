from sqlalchemy import select
from sqlalchemy.orm import Session

from src.budget_bot_2.models import Outcome
from src.budget_bot_2.repositories import OutcomeRepository
from tests.factories import TgUserFactory


async def test__save_record__success(add_category, test_session: Session):
    # Arrange
    tg_user = TgUserFactory()
    amount = 1000
    category = await add_category()

    # Act
    repo = OutcomeRepository(session=test_session)
    await repo.save_record(user=tg_user, amount=amount, category_name=category.name)

    # Assert
    result = await test_session.scalars(select(Outcome))
    records = result.all()
    assert len(records) == 1
    assert records[0].amount == amount
    assert records[0].category_id == category.id
