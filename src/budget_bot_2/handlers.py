from telegram.ext import ConversationHandler, MessageHandler, filters

from budget_bot_2.callbacks import MAIN_MENU  # write_income,; write_outcome,
from budget_bot_2.callbacks import (
    SELECTING_ACTION,
    SELECTING_CATEGORY,
    SELECTING_TYPE,
    WRITING_AMOUNT,
    WRITING_PEROID,
    choose_type,
    give_report,
    send_categories,
    send_report,
    start,
    write_amount,
    write_category,
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
        WRITING_PEROID: [MessageHandler(filters.Regex(r"\d+"), send_report)],
        SELECTING_TYPE: [
            MessageHandler(filters.Regex(r"(Доход)|(Расход)"), send_categories)
            # MessageHandler(filters.Regex("Расход"), write_outcome),
        ],
        SELECTING_CATEGORY: [MessageHandler(filters.TEXT, write_category)],
        WRITING_AMOUNT: [MessageHandler(filters.Regex(r"\d.?\d*"), write_amount)],
    },
    fallbacks=[start_handler],
)
