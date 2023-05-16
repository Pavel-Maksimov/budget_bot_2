from datetime import datetime

from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import (Column, BigInteger, Integer, ForeignKey, Numeric,
                        String, TIMESTAMP, CheckConstraint)


Base = declarative_base()


class Outcome(Base):
    """
    Outcome records.
    """

    __tablename__ = "outcome"
    __table_args__ = (
        CheckConstraint("amount >= 0.00", name="outcome_amount_positive"),
        CheckConstraint(
            "created_on >= CURRENT_TIMESTAMP",
            name="outcome_created_on_positive"
        )
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"))
    amount = Column(Numeric(precision=12, scale=2))
    category_id = Column(Integer, ForeignKey("outcome_category.id"))
    created_on = Column(TIMESTAMP(timezone=True), default=datetime.now())

    user = relationship("User", back_populates="outcomes")
    category = relationship(
        "OutcomeCategory",
        back_populates="outcomes"
    )


class Income(Base):
    """
    Income records.
    """

    __tablename__ = "income"
    __table_args__ = (
        CheckConstraint("amount >= 0.00", name="income_amount_positive"),
        CheckConstraint(
            "created_on >= CURRENT_TIMESTAMP",
            name="income_created_on_positive"
        )
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"))
    amount = Column(Numeric(precision=12, scale=2))
    category_id = Column(Integer, ForeignKey("income_category.id"))
    created_on = Column(TIMESTAMP(timezone=True))

    user = relationship("User", back_populates="incomes")
    category = relationship(
        "IncomeCategory",
        back_populates="incomes"
    )


class OutcomeCategory(Base):

    __tablename__ = "outcome_category"
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    records = relationship(
        "Outcome",
        backref=backref("category")
    )


class IncomeCategory(Base):

    __tablename__ = "income_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    records = relationship(
        "Income",
        backref=backref("category")
    )


class User(Base):

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    tg_username = Column(String(32))

    incomes = relationship("Income", backref=backref("user"))
    outcomes = relationship(
        "Outcome",
        backref=backref("user")
    )
