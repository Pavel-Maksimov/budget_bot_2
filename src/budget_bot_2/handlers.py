from telegram.ext import ConversationHandler, MessageHandler, filters

from budget_bot_2.callbacks import (
    MAIN_MENU,
    SELECTING_ACTION,
    SELECTING_CATEGORY,
    SELECTING_TYPE,
    WRITING_AMOUNT,
    choose_type,
    give_report,
    start,
    write_amount,
    write_category,
    write_income,
    write_outcome,
)

start_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), start)

conv_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        MAIN_MENU: [start_handler],
        SELECTING_ACTION: [
            MessageHandler(filters.Regex("Отчет"), give_report),
            MessageHandler(filters.Regex("Запись"), choose_type),
        ],
        SELECTING_TYPE: [
            MessageHandler(filters.Regex("Доход"), write_income),
            MessageHandler(filters.Regex("Расход"), write_outcome),
        ],
        SELECTING_CATEGORY: [MessageHandler(filters.TEXT, write_category)],
        WRITING_AMOUNT: [MessageHandler(filters.Regex(r"\d.?\d*"), write_amount)],
    },
    fallbacks=[start_handler],
)
