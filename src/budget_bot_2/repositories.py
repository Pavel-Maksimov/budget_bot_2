from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Income, IncomeCategory, Outcome, OutcomeCategory, User


class BaseRepository:
    """
    Base class for all repositories.

    Define initialization method, which takes
    one argument - session to connect to database.
    """

    def __init__(self, session: Session):
        self.session = session


class RecordRepository(BaseRepository):
    record = None
    category = None

    async def save_record(self, user, amount, category_name):
        category_id = await self.session.scalar(
            select(self.category.id).where(self.category.name == category_name)
        )
        user_repo = UserRepository(self.session)
        current_user = await user_repo.get_by_id(user.id)
        if not current_user:
            current_user = await user_repo.save_user(user)
        new_record = self.record(
            user_id=current_user.id,
            amount=amount,
            category_id=category_id,
            created_on=datetime.now(),
        )
        self.session.add(new_record)
        await self.session.commit()

    async def get_all_categories(self):
        result = await self.session.scalars(select(self.category.name))
        return result.all()

    async def get_grouped_by_day(self, period):
        self.session.execute(select(self.record))

    async def save_category(self, name):
        pass


class IncomeRepository(RecordRepository):
    record = Income
    category = IncomeCategory


class OutcomeRepository(RecordRepository):
    record = Outcome
    category = OutcomeCategory


class UserRepository(BaseRepository):
    async def save_user(self, user):
        new_user = User(
            tg_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            tg_username=user.username,
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_by_id(self, user_id):
        user = await self.session.execute(select(User).where(User.tg_id == user_id))
        return user.one()[0]
