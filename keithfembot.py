import calendar
import datetime as dt
import html
import logging
from http import HTTPStatus

import requests
from config import DADJOKE_URL, FORTUNE_URL, HTTP_API_TOKEN, KEITHFEM_BASE_URL
from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def send(update, context, msg):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=html.unescape(msg),
        parse_mode=ParseMode.MARKDOWN,
    )


def about(update, context):
    """ About """
    msg = (
        "Keith F'em, a community radio experiment, is presented by Keith "
        "in conjuction with SP2. `hello@keithfem.com`\n"
        "Bot created in Barcelona during the COVID-19 outbreak quarantine "
        "(March 2020) ✌"
    )
    send(update, context, msg)


def error(update, context):
    """ Log Errors """
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def parse_show(show):
    name = show["name"]
    starts = show["starts"][-8:-3]
    ends = show["ends"][-8:-3]
    return (
        starts,
        ends,
        name,
    )


def show(update, context, when):
    """ Displays the show that is on air at the moment. """
    response = requests.get(KEITHFEM_BASE_URL + "live-info")
    if response.status_code == HTTPStatus.OK:
        response = response.json()
        show = parse_show(response[when][0])  # just to shift the result
        send(update, context, "*%s* (%s - %s _🇩🇪 time!_)" % (show[2:] + show[:2]))
    else:
        send(update, context, "We cannot tell you at the moment.")


def now(update, context):
    """ Displays the show that is in the air now. """
    show(update, context, "currentShow")


def next(update, context):
    """ Displays the upcoming show. """
    show(update, context, "nextShow")


def day(update, context, on_day):
    """ Displays the schedule for the weekday on_day. """
    response = requests.get(KEITHFEM_BASE_URL + "week-info")
    if response.status_code == HTTPStatus.OK:
        response = response.json()
        shows_msg = ""
        for show in response[on_day.lower()]:
            shows_msg += "(%s - %s) - *%s*\n" % parse_show(show)
        msg = "Shows for %s _🇩🇪 time!_\n" % (on_day,)
        send(update, context, msg + shows_msg)
    else:
        send(update, context, "We cannot tell you at the moment.")


def schedule_day(update, context, timedelta):
    my_date = dt.date.today() + dt.timedelta(days=timedelta)
    day = calendar.day_name[my_date.weekday()]
    if timedelta and day == "Monday":  # week finishes on Sunday
        day = "next" + day
    day(update, context, day)


def today(update, context):
    """ Displays the schedule for today. """
    schedule_day(update, context, timedelta=0)


def tomorrow(update, context):
    """ Displays the schedule for tomorrow. """
    schedule_day(update, context, timedelta=1)


def week(update, context):
    """ Displays the schedule for the week. """
    days_of_the_week = []
    for day in range(0, 7):
        days_of_the_week.append(calendar.day_name[day].lower())
    response = requests.get(KEITHFEM_BASE_URL + "week-info")
    if response.status_code == HTTPStatus.OK:
        msg = ""
        response = response.json()
        for day in response:
            if day not in days_of_the_week:
                continue
            msg += "*Shows for %s*\n" % (day.capitalize(),)
            for show in response[day]:
                msg += "(%s - %s) - *%s*\n" % parse_show(show)
        msg += "_ All shows are in 🇩🇪 time!_"
        send(update, context, msg)
    else:
        send(update, context, "We cannot tell you at the moment.")


def gibberish(update, context):
    """ Displays a fortune. """
    response = requests.get(FORTUNE_URL)
    if response.status_code == HTTPStatus.OK:
        send(update, context, response.json())
    else:
        send(update, context, "Nothing to say about that.")


def beer(update, context):
    """ Beer ad """
    message = (
        "I'm gonna plug this right here. "
        "Our good friends at Berliner Berg are delivering "
        "crate of beer to your door, AND all of the money "
        "goes to support Keith. It's really cool of them.\n"
        "[https://tinyurl.com/keithsolikisten]\n"
        "Anyway, if you wanna drink some pale ale, "
        "get it here and help us out. Love y'all!\n"
    )
    send(update, context, message)


def joke(update, context):
    """ Tells a dad joke. """
    headers = {
        "User-Agent": "Keith F'em Bot (https://github.com/mazzi/keithfembot)",
        "Accept": "text/plain",
    }
    response = requests.get(DADJOKE_URL, headers=headers)
    if response.status_code == HTTPStatus.OK:
        send(update, context, response.text)
    else:
        send(update, context, "Nothing to say about that.")


def donate(update, context):
    """" Displays donate link """
    send(update, context, "[https://paypal.me/keithfem]")


def help(update, context):
    """ Help usage. """
    help_text = (
        "`/about`: the old and boring about command.\n"
        "`/now`: show what is on the air at the moment.\n"
        "`/next`: displays the upcoming show.\n"
        "`/today`: displays the schedule for today.\n"
        "`/tomorrow`: displays the schedule for tomorrow.\n"
        "`/week`: displays the shows for the week.\n"
        "`/gibberish`: some gibberish.\n"
        "`/beer`: do you want some beer uh?\n"
        "`/joke`: KeithF'em BotMeister, tell me a joke.\n"
        "`/donate`: donate to Keith F'em.\n"
        "`/help`: this help.\n"
    )
    send(update, context, help_text)


def main():
    """ Starts the bot. """
    updater = Updater(token=HTTP_API_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("now", now))
    dp.add_handler(CommandHandler("next", next))
    dp.add_handler(CommandHandler("today", today))
    dp.add_handler(CommandHandler("tomorrow", tomorrow))
    dp.add_handler(CommandHandler("week", week))
    dp.add_handler(CommandHandler("gibberish", gibberish))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("beer", beer))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("donate", donate))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
