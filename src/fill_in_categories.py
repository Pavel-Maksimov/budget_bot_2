"""
Initial insert queries for income and outcome categories.
"""

import asyncio

from budget_bot_2.db_connection import Session
from budget_bot_2.models import IncomeCategory, OutcomeCategory

INCOME_CATEGORIES = ["зарплата", "другое"]

OUTCOME_CATEGORIES = [
    "продукты",
    "общественный траспорт",
    "аптека",
    "кафе",
    "подписки",
    "развлечения",
    "бытовые расходы",
    "мобильная связь",
    "интернет",
    "животные",
    "коммунальные",
    "книги",
    "налоги",
    "автомобиль",
]


async def fill_in_categories():
    async with Session() as session:
        income_categories = [IncomeCategory(name=cat) for cat in INCOME_CATEGORIES]
        session.add_all(income_categories)
        outcome_caregories = [OutcomeCategory(name=cat) for cat in OUTCOME_CATEGORIES]
        session.add_all(outcome_caregories)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(fill_in_categories())
