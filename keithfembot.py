from config import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def about(update, context):
    """ About """
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    """ On noncommand i.e message - echo the message on Telegram"""
    update.message.reply_text(update.message.text)

def error(update, context):
    """ Log Errors """
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """ Start the bot. """
    updater = Updater(token=HTTP_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()