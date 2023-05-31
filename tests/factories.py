import factory
from telegram._user import User as TgUser

from budget_bot_2.models import OutcomeCategory, User
from fill_in_categories import OUTCOME_CATEGORIES
from tests.testing_db_connection import TestSession


class AbstractFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = TestSession


class TgUserFactory(factory.Factory):
    class Meta:
        model = TgUser

    id = factory.Sequence(int)
    first_name = factory.Faker("first_name")
    is_bot = False


class UserFactory(AbstractFactory):
    class Meta:
        model = User

    tg_id = factory.Sequence(int)
    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    tg_username = factory.Faker("user_name")


class OutcomeCategoryFactory(factory.Factory):
    class Meta:
        model = OutcomeCategory

    name = factory.Iterator(OUTCOME_CATEGORIES)
