import calendar
import datetime as dt
import html
from typing import Tuple, Union

import requests
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from config import DADJOKE_URL, KEITHFEM_BASE_URL
from exceptions import KeithFemException, NoShowException


class Command:
    """A Base class for all the bot commands."""

    def __init__(self, http_client=None, service_url=None):
        self.http_client = http_client
        self.service_url = service_url
        self.headers = None
        self.msg = None

    def __call__(
        self, update: Union[Update, None], context: Union[CallbackContext, None]
    ) -> str:
        self.send(update, context, self.msg)
        return self.msg

    def _get(self) -> Union[str, requests.Response]:
        """Gets info from external services"""
        return self.http_client.get(
            url=self.service_url,
            headers=self.headers,
        )

    def _parse(self, show) -> Tuple[str, str, str]:
        """Parses show name, start and end.

        Args:
            show (dict): A dictionary with a name and start and end of a show.

        Returns:
            tuple: A tuple with start time, end time and name of the show (un-scaped)
        """
        name = show["name"]
        starts = show["starts"][-8:-3]
        ends = show["ends"][-8:-3]
        return (
            starts,
            ends,
            html.unescape(name),
        )

    def _format(self, show) -> str:
        """Formats a show info to be ready to be send

        Args:
            show (tuple): ("01:00", "04:00", "name")

        Returns:
            str: a show name in bold, and start and end time. Example:
                Nocturnal Emissions (01:00 - 04:00 🇩🇪 time!)
        """
        return "*%s* (%s - %s _🇩🇪 time!_)" % (show[2:] + show[:2])

    def send(
        self,
        update: Union[Update, None],
        context: Union[CallbackContext, None],
        msg=None,
    ) -> None:
        """Send method from python-telegram-bot"""
        context.bot.send_message(  # type: ignore
            chat_id=update.effective_chat.id,  # type: ignore
            text=msg or self.msg,
            parse_mode=ParseMode.MARKDOWN,
        )
        return msg or self.msg


class About(Command):
    """Displays the information about the KeithFemBot"""

    def __init__(self):
        super().__init__()
        self.msg = (
            "Keith F'em, a community radio experiment, is presented by Keith "
            "in conjunction with SP2. `hello@keithfem.com`\n"
            "Bot created in Barcelona during the COVID-19 outbreak quarantine "
            "(March 2020) ✌️"
        )


class Donate(Command):
    """Displays link to donate to Keith F'em"""

    def __init__(self):
        super().__init__()
        self.msg = "[https://www.paypal.me/keithfem]"


class Help(Command):
    """Help usage."""

    def __init__(self):
        super().__init__()
        self.msg = (
            "`/about`: the old and boring about command.\n"
            "`/now`: show what is on the air at the moment.\n"
            "`/next`: displays the upcoming show.\n"
            "`/today`: displays the schedule for today.\n"
            "`/tomorrow`: displays the schedule for tomorrow.\n"
            "`/week`: displays the shows for the week.\n"
            "`/joke`: KeithF'em BotMeister, tell me a joke.\n"
            "`/donate`: donate to Keith F'em.\n"
            "`/help`: this help.\n"
        )


class Joke(Command):
    """Tells a dad joke."""

    def __init__(self, http_client, service_url=None, headers=None):
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or DADJOKE_URL
        self.headers = headers or {
            "User-Agent": "Keith F'em Bot (https://github.com/mazzi/keithfembot)",
            "Accept": "text/plain",
        }

    def __call__(
        self, update: Union[Update, None], context: Union[CallbackContext, None]
    ) -> str:

        msg = str(self._get())
        self.send(update, context, msg)
        return msg


class ShowCommand(Command):
    """Base class for single show display"""

    def __init__(self, node, http_client, service_url=None):
        """Constructor

        Args:
            node (str): A node in the response to be parsed.
            http_client (Any): mock compatible with requests
            service_url (str, optional): Url of the service to hit (airtime).
                Defaults to KEITHFEM_BASE_URL + 'live-info'.
        """
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "live-info"
        self.node = node
        self.no_show_message = ""

    def _parse(self, show) -> Tuple[str, str, str]:
        # Only Parse if the show is today or tomorrow
        today = dt.date.today().weekday()
        tomorrow = (dt.date.today() + dt.timedelta(days=1)).weekday()
        day_of_show = dt.datetime.strptime(
            show["starts"], "%Y-%m-%d %H:%M:%S"
        ).weekday()

        if day_of_show not in [today, tomorrow]:
            raise NoShowException

        return super()._parse(show)

    def __call__(
        self, update: Union[Update, None], context: Union[CallbackContext, None]
    ) -> str:
        response = self._get()
        if isinstance(response, requests.Response):
            response = response.json()
        else:
            raise KeithFemException(
                "Unexpected answer from service (%s)", self.__class__.__name__
            )

        try:
            msg = self._format(self._parse(response[self.node][0]))  # type: ignore
        except (IndexError, NoShowException):
            msg = (
                self.no_show_message + "\nCheck the weekly schedule with /week command."
            )

        self.send(update, context, msg)
        return msg


class Now(ShowCommand):
    """Displays the show that is on air at the moment."""

    def __init__(self, http_client, service_url=None, node="currentShow"):
        super().__init__(
            node=node,
            http_client=http_client,
            service_url=service_url,
        )
        self.no_show_message = "Nothing being broadcasted at the moment 🥺."


class Next(ShowCommand):
    """Displays the show that comes after the current one on air."""

    def __init__(self, http_client, service_url=None, node="nextShow"):
        super().__init__(
            node=node,
            http_client=http_client,
            service_url=service_url,
        )
        self.no_show_message = "Nothing else scheduled for today 🥺."


class DayCommand(Command):
    """Base class for daily show display"""

    def __init__(self, http_client, service_url=None):
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "week-info"
        self.no_shows_message = ""
        self.on_day = None

    def _parse_response(self, response, day) -> str:
        """From a response, it returns a string with the shows of the day

        Args:
            response (dict): A dict with the shows for the week.
            day (str): day of the week to be parsed

        Returns:
            str: A string with all the shows for the day
        """
        shows_msg = ""
        for show in response[day.lower()]:
            shows_msg += "(%s - %s) - *%s*\n" % super()._parse(show)
        return shows_msg

    def _format(self, day) -> str:
        return "Shows for %s _🇩🇪 time!_\n" % (day.replace("next", "")).capitalize()

    def __call__(
        self, update: Union[Update, None], context: Union[CallbackContext, None]
    ) -> str:
        response = self._get()
        if isinstance(response, requests.Response):
            response = response.json()
        else:
            raise KeithFemException(
                "Unexpected answer from service (%s)", self.__class__.__name__
            )

        shows = self._parse_response(response, self.on_day)
        if shows:
            msg = self._format(self.on_day) + shows
        else:
            msg = (
                self.no_shows_message
                + "\nCheck the weekly schedule with /week command."
            )

        self.send(update, context, msg)
        return msg


class Today(DayCommand):
    """Displays the radio schedule for today"""

    def __init__(self, http_client, service_url=None):
        super().__init__(http_client, service_url)
        today = dt.date.today()
        self.on_day = calendar.day_name[today.weekday()].lower()
        self.no_shows_message = "No shows are scheduled for today 🤷."


class Tomorrow(DayCommand):
    """Displays the radio schedule for tomorrow"""

    def __init__(self, http_client, service_url=None):
        super().__init__(http_client, service_url)
        tomorrow = dt.date.today() + dt.timedelta(days=1)
        self.on_day = calendar.day_name[tomorrow.weekday()].lower()
        # if tomorrow is monday, fetches 'nextmonday' on the array
        if self.on_day.lower() == calendar.day_name[calendar.firstweekday()].lower():
            self.on_day = "next" + self.on_day
        self.no_shows_message = "No shows are scheduled for tomorrow 🤷."


class Week(Command):
    """Displays the radio schedule for the week"""

    def __init__(self, http_client, service_url=None):
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "week-info"
        self.no_shows_message = (
            "No shows for the week. This day should haven't arrived. 😭"
        )

    def _parse_response(self, response) -> str:
        """From a response, it returns the shows for the week

        Args:
            response (dict): A dict with the shows for the week.

        Returns:
            str: A string with all the shows for the week
        """
        msg = ""
        days_of_the_week = []
        for day_number in range(0, 7):
            days_of_the_week.append(calendar.day_name[day_number].lower())

        for day in response:
            if day not in days_of_the_week:
                continue
            shows = ""
            for show in response[day]:
                shows += "(%s - %s) - *%s*\n" % super()._parse(show)
            if shows:
                msg += "*Shows for %s*\n" % (day.capitalize(),) + shows
        if msg:
            msg += "_ All shows are in 🇩🇪 time!_"
        else:
            msg = self.no_shows_message

        return msg

    def __call__(
        self, update: Union[Update, None], context: Union[CallbackContext, None]
    ) -> str:

        response = self._get()
        if isinstance(response, requests.Response):
            response = response.json()
        else:
            raise KeithFemException(
                "Unexpected answer from service (%s)", self.__class__.__name__
            )

        msg = self._parse_response(response)

        self.send(update, context, msg)
        return msg
