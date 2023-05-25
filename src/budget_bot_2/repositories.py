from datetime import datetime, timedelta

from sqlalchemy import Date, cast, desc, func, select
from sqlalchemy.orm import Session

from budget_bot_2.custom_exeptions import RequestNotSuccessError
from budget_bot_2.models import Income, IncomeCategory, Outcome, OutcomeCategory, User


class BaseRepository:
    """
    Base class for all repositories.

    Define initialization method, which takes
    one argument - session to connect to database.
    """

    def __init__(self, session: Session):
        self.session = session


class RecordRepository(BaseRepository):
    record: Income = None
    category: IncomeCategory = None

    async def save_record(self, user, amount, category_name):
        category_id = await self.session.scalar(
            select(self.category.id).where(self.category.name == category_name)
        )
        if category_id is None:
            raise RequestNotSuccessError("Нет такой категории")
        user_repo = UserRepository(self.session)
        current_user = await user_repo.get_by_tg_id(user.id)
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

    async def get_grouped_by_day(self, user_id, period):
        result = await self.session.execute(
            select(
                cast(self.record.created_on, Date),
                func.sum(self.record.amount),
            )
            .join(User, User.tg_id == user_id)
            .where(self.record.created_on > (func.now() - timedelta(days=period)))
            .group_by(cast(self.record.created_on, Date))
            .order_by(cast(self.record.created_on, Date))
        )
        return result.all()

    async def get_ungrouped(self, user_id, period):
        result = await self.session.execute(
            select(self.record.created_on, self.category.name, self.record.amount)
            .join(self.category)
            .join(User, User.tg_id == user_id)
            .where(self.record.created_on > (func.now() - timedelta(days=period)))
            .order_by("created_on")
        )
        return result.all()

    async def get_grouped_by_categories(self, user_id, period):
        result = await self.session.execute(
            select(
                self.category.name,
                func.sum(self.record.amount).label("amount"),
            )
            .join(self.category)
            .join(User, User.tg_id == user_id)
            .where(self.record.created_on > (func.now() - timedelta(days=period)))
            .group_by(self.category.name)
            .order_by(desc("amount"))
        )
        return result.all()

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

    async def get_by_tg_id(self, user_id):
        user = await self.session.execute(select(User).where(User.tg_id == user_id))
        return user.one()[0]
