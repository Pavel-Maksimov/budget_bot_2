"""
Models represent tables on the database.

Fields of models define their columns.
"""
from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import backref, declarative_base, relationship

Base = declarative_base()


class Outcome(Base):
    """
    Outcome records.
    """

    __tablename__ = "outcome"
    __table_args__ = (
        CheckConstraint("amount >= 0.00", name="outcome_amount_positive"),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"))
    amount = Column(Numeric(precision=12, scale=2))
    category_id = Column(Integer, ForeignKey("outcome_category.id"))
    created_on = Column(TIMESTAMP(timezone=True), default=datetime.now())

    user = relationship("User", back_populates="outcomes")
    category = relationship("OutcomeCategory", back_populates="records")

    def __repr__(self) -> str:
        return f"Outcome {self.category.name}"


class Income(Base):
    """
    Income records.
    """

    __tablename__ = "income"
    __table_args__ = (CheckConstraint("amount >= 0.00", name="income_amount_positive"),)

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"))
    amount = Column(Numeric(precision=12, scale=2))
    category_id = Column(Integer, ForeignKey("income_category.id"))
    created_on = Column(TIMESTAMP(timezone=True))

    user = relationship("User", back_populates="incomes")

    def __repr__(self) -> str:
        return f"Income {self.id}"


class OutcomeCategory(Base):

    __tablename__ = "outcome_category"
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    records = relationship("Outcome")

    def __repr__(self) -> str:
        return f"Outcome category {self.name}"


class IncomeCategory(Base):

    __tablename__ = "income_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    records = relationship("Income", backref=backref("category"))

    def __repr__(self) -> str:
        return f"Income category {self.name}"


class User(Base):

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    tg_username = Column(String(32))

    incomes = relationship("Income")
    outcomes = relationship("Outcome")

    def __repr__(self) -> str:
        return f"User {self.first_name}, {self.tg_id}"
