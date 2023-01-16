import calendar
import datetime as dt
import html

from telegram import ParseMode

from config import DADJOKE_URL, KEITHFEM_BASE_URL


class Command:
    """A Base class for all the bot commands."""

    def __init__(self):
        self.service_url = None
        self.headers = None

    def __call__(self, update, context) -> str:
        raise NotImplementedError

    def _get(self) -> str:
        """Gets info from external services"""
        return self.http_client.get(
            url=self.service_url,
            headers=self.headers,
        )

    def _parse_show(self, show) -> str:
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

    def _format_show(self, show) -> str:
        """Formats a show info to be ready to be send

        Args:
            show (tuple): ("01:00", "04:00", "name")

        Returns:
            str: a show name in bold, and start and end time. Example:
                Nocturnal Emissions (01:00 - 04:00 🇩🇪 time!)
        """
        return "*%s* (%s - %s _🇩🇪 time!_)" % (show[2:] + show[:2])

    def send(update, context, msg) -> None:
        """Send method from python-telegram-bot"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg,
            parse_mode=ParseMode.MARKDOWN,
        )


class About(Command):
    """Displays the information about the KeithFemBot"""

    def __init__(self):
        super().__init__()

    def __call__(self, update, context):
        msg = (
            "Keith F'em, a community radio experiment, is presented by Keith "
            "in conjunction with SP2. `hello@keithfem.com`\n"
            "Bot created in Barcelona during the COVID-19 outbreak quarantine "
            "(March 2020) ✌️"
        )
        self.send(update, context, msg)
        return msg


class Donate(Command):
    """Displays link to donate to Keith F'em"""

    def __init__(self):
        super().__init__()

    def __call__(self, update, context) -> str:
        msg = "[https://www.paypal.me/keithfem]"
        self.send(update, context, msg)
        return msg


class Help(Command):
    """Help usage."""

    def __init__(self):
        super().__init__()

    def __call__(self, update, context) -> str:
        msg = (
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
        self.send(update, context, msg)
        return msg


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

    def __call__(self, update, context) -> str:

        msg = self._get()
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

    def __call__(self, update, context) -> str:
        response = self._get().json()
        msg = self._format_show(self._parse_show(response[self.node][0]))

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


class Next(ShowCommand):
    """Displays the show that comes after the current one on air."""

    def __init__(self, http_client, service_url=None, node="nextShow"):
        super().__init__(
            node=node,
            http_client=http_client,
            service_url=service_url,
        )


class DayCommand(Command):
    """Base class for daily show display"""

    def __init__(self, http_client, service_url=None):
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "week-info"

    def _parse(self, response, day) -> str:
        """From a response, it returns a string with the shows of the day

        Args:
            response (dict): A dict with the shows for the week.
            day (str): day of the week to be parsed

        Returns:
            str: A string with all the shows for the day
        """
        shows_msg = ""
        for show in response[day.lower()]:
            shows_msg += "(%s - %s) - *%s*\n" % self._parse_show(show)
        return shows_msg


class Today(DayCommand):
    """Displays the radio schedule for today"""

    def __init__(self, http_client, service_url=None):
        super().__init__(http_client, service_url)

    def __call__(self, update, context) -> str:
        today = dt.date.today()
        on_day = calendar.day_name[today.weekday()].lower()

        response = self._get().json()
        shows = self._parse(response, on_day)

        msg = "Shows for %s _🇩🇪 time!_\n" % (on_day.capitalize(),) + shows

        self.send(update, context, msg)
        return msg


class Tomorrow(DayCommand):
    """Displays the radio schedule for tomorrow"""

    def __init__(self, http_client, service_url=None):
        super().__init__(http_client, service_url)

    def __call__(self, update, context) -> str:
        tomorrow = dt.date.today() + dt.timedelta(days=1)
        on_day = calendar.day_name[tomorrow.weekday()].lower()

        # if tomorrow is monday, fetches 'nextmonday' on the array
        if on_day.lower() == calendar.day_name[calendar.firstweekday()].lower():
            on_day = "next" + on_day

        response = self._get().json()
        shows = self._parse(response, on_day)

        msg = (
            "Shows for %s _🇩🇪 time!_\n" % (on_day.replace("next", "").capitalize(),)
            + shows
        )

        self.send(update, context, msg)
        return msg


class Week(Command):
    """Displays the radio schedule for the week"""

    def __init__(self, http_client, service_url=None):
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "week-info"

    def _parse(self, response) -> str:
        """From a response, it returns the shows for the week

        Args:
            response (dict): A dict with the shows for the week.

        Returns:
            str: A string with all the shows for the week
        """
        msg = ""
        days_of_the_week = []
        for day in range(0, 7):
            days_of_the_week.append(calendar.day_name[day].lower())

        for day in response:
            if day not in days_of_the_week:
                continue
            msg += "*Shows for %s*\n" % (day.capitalize(),)
            for show in response[day]:
                msg += "(%s - %s) - *%s*\n" % self._parse_show(show)
        msg += "_ All shows are in 🇩🇪 time!_"

        return msg

    def __call__(self, update, context) -> str:

        response = self._get().json()
        msg = self._parse(response)

        self.send(update, context, msg)
        return msg
