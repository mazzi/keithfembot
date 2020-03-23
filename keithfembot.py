from config import *
import html
import random
import requests
import datetime as dt
import calendar
from http import HTTPStatus
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

DAYS = ['monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday']

def send(update, context, msg):
    context.bot.send_message(chat_id=update.effective_chat.id, text=html.unescape(msg), parse_mode=ParseMode.MARKDOWN)

def about(update, context):
    """ About """
    msg = "Keith F'em, a community radio experiment, is presented by Keith in conjuction with SP2. `hello@keithfem.com`\n"
    msg += "Bot created in Barcelona during the COVID-19 outbreak quarantine (March 2020) ✌"
    send(update, context, msg)

def echo(update, context):
    """ On noncommand i.e message - echo the message on Telegram"""
    update.message.reply_text(update.message.text)

def error(update, context):
    """ Log Errors """
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def show(update, context, when):
    """ Displays the show that is on air at the moment. """
    response = requests.get(KEITHFEM_BASE_URL + "live-info")
    if response.status_code == HTTPStatus.OK:
        response = response.json()
        name = response[when][0]['name']
        starts = response[when][0]['starts'][-8:-3]
        ends = response[when][0]['ends'][-8:-3]
        send(update, context, "*%s*, (%s - %s 🇩🇪 time!_)" % (name, starts, ends,))
    else:
        send(update, context, "We cannot tell you at the moment.")

def now(update, context):
    show(update,context, 'currentShow')

def next(update, context):
    """ Displays the upcoming show. """
    show(update, context, 'nextShow')

def day(update,context, on_day):
    response = requests.get(KEITHFEM_BASE_URL + "week-info")
    if response.status_code == HTTPStatus.OK:
        response = response.json()
        shows_msg = ""
        for show in response[on_day.lower()]:
            name = show['name']
            starts = show['starts'][-8:-3]
            ends = show['ends'][-8:-3]
            shows_msg += "(%s - %s) - *%s*\n" % (starts, ends, name,)
        msg = "Shows for %s _🇩🇪 time!_\n" % (on_day,)
        send(update, context, msg + shows_msg)
    else:
        send(update, context, "We cannot tell you at the moment.")

def today(update, context):
    """ Displays the schedule for today. """
    my_date = dt.date.today()
    today = calendar.day_name[my_date.weekday()]
    day(update, context, today)

def tomorrow(update, context):
    """ Displays the schedule for tomorrow. """
    my_date = dt.date.today() + dt.timedelta(days=1)
    tomorrow = calendar.day_name[my_date.weekday()]
    day(update, context, tomorrow)

def week(update, context):
    """ Displays the schedule for the week. """
    response = requests.get(KEITHFEM_BASE_URL + "week-info")
    if response.status_code == HTTPStatus.OK:
        msg = ""
        response = response.json()
        for day in response:
            if day not in DAYS:
                continue
            msg += "*Shows for %s*\n" % (day.capitalize(),)
            for show in response[day]:
                name = show['name']
                starts = show['starts'][-8:-3]
                ends = show['ends'][-8:-3]
                msg += "(%s - %s) - *%s*\n" % (starts, ends, name,)
        msg += "_ All shows are in 🇩🇪 time!_"
        send(update, context, msg)
    else:
        send(update, context, "We cannot tell you at the moment.")

def gibberish(update, context):
    response = requests.get(FORTUNE_URL)
    if response.status_code == HTTPStatus.OK:
        send(update, context, response.json())
    else:
        send(update, context, "Nothing to say about that.")

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