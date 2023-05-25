from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from budget_bot_2.custom_exeptions import RequestNotSuccessError
from budget_bot_2.db_connection import Session
from budget_bot_2.report import create_report
from budget_bot_2.repositories import IncomeRepository, OutcomeRepository
from budget_bot_2.utilities import create_keyboard

SELECTING_ACTION = "action"
MAIN_MENU = "menu"
WRITING_RECORD = "record"
SELECTING_TYPE = "type"
SELECTING_CATEGORY = "category"
WRITING_AMOUNT = "amount"
WRITING_PEROID = "period"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Выберите действие"
    keyboard = [["Запись", "Отчет"]]
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return SELECTING_ACTION


async def give_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Введите период в днях"
    await update.message.reply_text(text=text)
    return WRITING_PEROID


async def send_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        report_path = await create_report(
            user_id=update.effective_user.id, period=int(update.message.text)
        )
        await update.message.reply_document(document=report_path)
    except RequestNotSuccessError as err:
        await update.message.reply_text(text=err.message)
    return -1


async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Выберите тип записи"
    keyboard = [["Доход", "Расход"]]
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return SELECTING_TYPE


async def send_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["record"] = update.message.text
    async with Session() as session:
        if update.message.text == "Доход":
            repo = IncomeRepository(session)
        else:
            repo = OutcomeRepository(session)
        categories = await repo.get_all_categories()
    text = "Выберите категорию"
    keyboard = create_keyboard(3, categories)
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return SELECTING_CATEGORY


async def write_outcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["record"] = update.message.text
    text = "Выберите категорию"
    async with Session() as session:
        categories = await OutcomeRepository(session).get_all_categories()
    keyboard = create_keyboard(3, categories)
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return SELECTING_CATEGORY


async def write_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = update.message.text
    text = "Введите сумму"
    keyboard = create_keyboard(1, [])
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return WRITING_AMOUNT


async def write_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with Session() as session:
        if context.user_data["record"] == "Доход":
            repo = IncomeRepository(session)
        else:
            repo = OutcomeRepository(session)
        try:
            await repo.save_record(
                user=update.effective_user,
                amount=update.message.text,
                category_name=context.user_data["category"],
            )
            await update.message.reply_text(text="Записано!")
        except RequestNotSuccessError as err:
            await update.message.reply_text(text=err.message)
    return -1


async def save_record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="Записано!")
    return -1
