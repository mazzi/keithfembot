from config import *
from telegram.ext import Updater, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=HTTP_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


dispatcher.add_handler(CommandHandler('about', about))

updater.start_polling()