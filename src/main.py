import logging

from telegram.ext import ApplicationBuilder

import settings
from budget_bot_2.handlers import conv_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

app = ApplicationBuilder().token(settings.settings.BOT_TOKEN).build()
app.add_handler(conv_handler)
app.run_polling()
