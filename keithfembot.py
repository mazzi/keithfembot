from config import *
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

gibberish_phrase = ["Good things come to those who wait.",
                    "Patience is a virtue.",
                    "The early bird gets the worm.",
                    "A wise man once said, everything in its own time and place.",
                    "Fortune cookies rarely share fortunes."]

def send(msg):
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def about(update, context):
    """ About """
    send("Keith F'em, a community radio experiment, is presented by Keith in conjuction with SP2. hello@keithfem.com")
    send("Author: lmazzitelli@pm.me - Coded in Barcelona during the COVID-19 outbreak.")

def echo(update, context):
    """ On noncommand i.e message - echo the message on Telegram"""
    update.message.reply_text(update.message.text)

def error(update, context):
    """ Log Errors """
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def current(update, context):
    """ Displays the show that is on air at the moment. """
    pass

def now(update, context):
    """ Displays the show that is on air at the moment. """
    pass

def next(update, context):
    """ Displays the upcoming show. """
    pass

def today(update, context):
    """ Displays the schedule for today. """
    pass

def tomorrow(update, context):
    """ Displays the schedule for tomorrow. """
    pass

def week(update, context):
    """ Displays the schedule for the week. """
    pass

def gibberish(update, context):
    send(random.choice(gibberish_phrase))

def main():
    """ Start the bot. """
    updater = Updater(token=HTTP_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CommandHandler('current', current))
    dp.add_handler(CommandHandler('now', now))
    dp.add_handler(CommandHandler('next', next))
    dp.add_handler(CommandHandler('today', today))
    dp.add_handler(CommandHandler('tomorrow', tomorrow))
    dp.add_handler(CommandHandler('week', week))
    dp.add_handler(CommandHandler('gibberish', gibberish))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()