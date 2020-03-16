from config import *
import random
import requests
from http import HTTPStatus
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

gibberish_phrase = ["_Good things come to those who wait._",
                    "_Patience is a virtue._",
                    "_The early bird gets the worm._",
                    "_A wise man once said, everything in its own time and place._",
                    "_Fortune cookies rarely share fortunes._"]

def send(update, context, msg):
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=ParseMode.MARKDOWN)

def about(update, context):
    """ About """
    send(update, context, "Keith F'em, a community radio experiment, is presented by Keith in conjuction with SP2. `hello@keithfem.com`")
    send(update, context, "Bot created in Barcelona during the COVID-19 outbreak quarantine.")

def echo(update, context):
    """ On noncommand i.e message - echo the message on Telegram"""
    update.message.reply_text(update.message.text)

def error(update, context):
    """ Log Errors """
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def now(update, context):
    """ Displays the show that is on air at the moment. """
    response = requests.get("https://keithfem2.airtime.pro/api/live-info")
    if response.status_code == 200:
        response = response.json()
        logger.info(response)
        name = response['currentShow'][0]['name']
        starts = response['currentShow'][0]['starts'][-8:-3]
        ends = response['currentShow'][0]['ends'][-8:-3]
        send(update, context, "*%s*, (_starts: %s, ends: %s 🇩🇪 time!_)" % (name, starts, ends,))
    else:
        send(update, context, "We cannot tell you at the moment.")

def next(update, context):
    """ Displays the upcoming show. """
    send(update, context, "not done yet!")

def today(update, context):
    """ Displays the schedule for today. """
    send(update, context, "not done yet!")

def tomorrow(update, context):
    """ Displays the schedule for tomorrow. """
    send(update, context, "not done yet!")

def week(update, context):
    """ Displays the schedule for the week. """
    KEITHFEM_BASE_URL + "week-info"
    send(update, context, "not done yet!")

def gibberish(update, context):
    send(update, context, random.choice(gibberish_phrase))

def help(update, context):
    """ Help usage. """
    help_text=(
        "`/about`: the old and boring about command.\n"
        "`/now`: show what is on the air at the moment.\n"
        "`/next`: displays the upcoming show.\n"
        "`/today`: displays the schedule for today.\n"
        "`/tomorrow`: displays the schedule for tomorrow.\n"
        "`/week`: displays the shows for the week.\n"
        "`/gibberish`: some gibberish.\n"
        "`/help`: this help.\n"
    )
    send(update, context, help_text)

def main():
    """ Start the bot. """
    updater = Updater(token=HTTP_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CommandHandler('now', now))
    dp.add_handler(CommandHandler('next', next))
    dp.add_handler(CommandHandler('today', today))
    dp.add_handler(CommandHandler('tomorrow', tomorrow))
    dp.add_handler(CommandHandler('week', week))
    dp.add_handler(CommandHandler('gibberish', gibberish))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()