import calendar
import datetime as dt
import html
import logging
from http import HTTPStatus

import requests
from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

from config import DADJOKE_URL, FORTUNE_URL, HTTP_API_TOKEN, KEITHFEM_BASE_URL

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class KeithFemBotCommands:
    def _send(self, update, context, msg):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg,
            parse_mode=ParseMode.MARKDOWN,
        )

    def about(self, update, context):
        """About"""
        msg = (
            "Keith F'em, a community radio experiment, is presented by Keith "
            "in conjuction with SP2. `hello@keithfem.com`\n"
            "Bot created in Barcelona during the COVID-19 outbreak quarantine "
            "(March 2020) ✌"
        )
        self._send(update, context, msg)

    def error(self, update, context):
        """Log Errors"""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def _parse_show(self, show):
        """Parses show name, start and end."""
        name = show["name"]
        starts = show["starts"][-8:-3]
        ends = show["ends"][-8:-3]
        return (
            starts,
            ends,
            html.unescape(name),
        )

    def _show(self, update, context, when):
        """Displays the show that is on air at the moment."""
        response = requests.get(KEITHFEM_BASE_URL + "live-info")
        if response.status_code == HTTPStatus.OK:
            response = response.json()
            show = self._parse_show(response[when][0])  # just to shift the result
            self._send(
                update, context, "*%s* (%s - %s _🇩🇪 time!_)" % (show[2:] + show[:2])
            )
        else:
            self._send(update, context, "We cannot tell you at the moment.")

    def now(self, update, context):
        """Displays the show that is in the air now."""
        self._show(update, context, "currentShow")

    def next(self, update, context):
        """Displays the upcoming show."""
        self._show(update, context, "nextShow")

    def day(self, update, context, on_day):
        """Displays the schedule for the weekday on_day."""
        response = requests.get(KEITHFEM_BASE_URL + "week-info")
        if response.status_code == HTTPStatus.OK:
            response = response.json()
            shows_msg = ""
            for show in response[on_day.lower()]:
                shows_msg += "(%s - %s) - *%s*\n" % self._parse_show(show)
            msg = "Shows for %s _🇩🇪 time!_\n" % (on_day.replace("next", ""),)
            self._send(update, context, msg + shows_msg)
        else:
            self._send(update, context, "We cannot tell you at the moment.")

    def _schedule_day(self, update, context, timedelta):
        my_date = dt.date.today() + dt.timedelta(days=timedelta)
        on_day = calendar.day_name[my_date.weekday()]
        if timedelta and on_day == calendar.day_name[calendar.firstweekday()]:
            on_day = "next" + on_day
        self.day(update, context, on_day)

    def today(self, update, context):
        """Displays the schedule for today."""
        self._schedule_day(update, context, timedelta=0)

    def tomorrow(self, update, context):
        """Displays the schedule for tomorrow."""
        self._schedule_day(update, context, timedelta=1)

    def week(self, update, context):
        """Displays the schedule for the week."""
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
                    msg += "(%s - %s) - *%s*\n" % self._parse_show(show)
            msg += "_ All shows are in 🇩🇪 time!_"
            self._send(update, context, msg)
        else:
            self._send(update, context, "We cannot tell you at the moment.")

    def gibberish(self, update, context):
        """Displays a fortune."""
        response = requests.get(FORTUNE_URL)
        if response.status_code == HTTPStatus.OK:
            self._send(update, context, response.json())
        else:
            self._send(update, context, "Nothing to say about that.")

    def joke(self, update, context):
        """Tells a dad joke."""
        headers = {
            "User-Agent": "Keith F'em Bot (https://github.com/mazzi/keithfembot)",
            "Accept": "text/plain",
        }
        response = requests.get(DADJOKE_URL, headers=headers)
        if response.status_code == HTTPStatus.OK:
            self._send(update, context, response.text)
        else:
            self._send(update, context, "Nothing to say about that.")

    def donate(self, update, context):
        """Displays donate link"""
        self._send(
            update,
            context,
            "[https://www.paypal.me/keithfem]",
        )

    def help(self, update, context):
        """Help usage."""
        help_text = (
            "`/about`: the old and boring about command.\n"
            "`/now`: show what is on the air at the moment.\n"
            "`/next`: displays the upcoming show.\n"
            "`/today`: displays the schedule for today.\n"
            "`/tomorrow`: displays the schedule for tomorrow.\n"
            "`/week`: displays the shows for the week.\n"
            "`/togo`: info to order drinks.\n"
            "`/gibberish`: some gibberish.\n"
            "`/joke`: KeithF'em BotMeister, tell me a joke.\n"
            "`/donate`: donate to Keith F'em.\n"
            "`/help`: this help.\n"
        )
        self._send(update, context, help_text)


def main():
    """Starts the bot."""
    updater = Updater(token=HTTP_API_TOKEN, use_context=True)

    dp = updater.dispatcher

    KFBC = KeithFemBotCommands()

    dp.add_handler(CommandHandler("about", KFBC.about))
    dp.add_handler(CommandHandler("now", KFBC.now))
    dp.add_handler(CommandHandler("next", KFBC.next))
    dp.add_handler(CommandHandler("today", KFBC.today))
    dp.add_handler(CommandHandler("tomorrow", KFBC.tomorrow))
    dp.add_handler(CommandHandler("week", KFBC.week))
    dp.add_handler(CommandHandler("gibberish", KFBC.gibberish))
    dp.add_handler(CommandHandler("help", KFBC.help))
    dp.add_handler(CommandHandler("joke", KFBC.joke))
    dp.add_handler(CommandHandler("donate", KFBC.donate))
    dp.add_error_handler(KFBC.error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
