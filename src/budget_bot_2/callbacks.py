from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from budget_bot_2.db_connection import Session
from budget_bot_2.repositories import IncomeRepository, OutcomeRepository
from budget_bot_2.utilities import create_keyboard

SELECTING_ACTION = "action"
MAIN_MENU = "menu"
WRITING_RECORD = "record"
SELECTING_TYPE = "type"
SELECTING_CATEGORY = "category"
WRITING_AMOUNT = "amount"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Выберите действие"
    keyboard = [["Запись", "Отчет"]]
    await update.message.reply_text(
        text=text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return SELECTING_ACTION


async def give_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Недоступно)"
    await update.message.reply_text(text=text)
    return SELECTING_ACTION


async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Выберите тип записи"
    keyboard = [["Доход", "Расход"]]
    await update.message.reply_text(
        text=text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return SELECTING_TYPE


async def write_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["record"] = update.message.text
    text = "Выберите категорию"
    async with Session() as session:
        categories = await IncomeRepository(session).get_all_categories()
    keyboard = await create_keyboard(3, categories)
    await update.message.reply_text(
        text=text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return SELECTING_CATEGORY


async def write_outcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["record"] = update.message.text
    text = "Выберите категорию"
    async with Session() as session:
        categories = await OutcomeRepository(session).get_all_categories()
    keyboard = await create_keyboard(3, categories)
    await update.message.reply_text(
        text=text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return SELECTING_CATEGORY


async def write_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = update.message.text
    text = "Введите сумму"
    keyboard = await create_keyboard(1, [])
    await update.message.reply_text(
        text=text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return WRITING_AMOUNT


async def write_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with Session() as session:
        if context.user_data["record"] == "Доход":
            repo = IncomeRepository(session)
        else:
            repo = OutcomeRepository(session)
        await repo.save_record(
            user=update.effective_user,
            amount=update.message.text,
            category_name=context.user_data["category"],
        )
    await update.message.reply_text(text="Записано!")
    return -1


async def save_record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="Записано!")
    return -1
