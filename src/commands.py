import calendar
import datetime as dt

from telegram import ParseMode

from config import DADJOKE_URL, KEITHFEM_BASE_URL
from helpers import ParseHelper


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


class Now(Command):
    """Displays the show that is on air at the moment."""

    def __init__(self, http_client, service_url=None, node=None):
        """Constructor

        Args:
            http_client (Any): mock compatible with requests
            service_url (str, optional): Url of the service to hit (airtime).
                Defaults to KEITHFEM_BASE_URL + 'live-info'.
            node (str, optional): A node in the response to be parsed.
                Defaults to 'currentShow'.
        """
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "live-info"
        self.node = node or "currentShow"

    def __call__(self, update, context) -> str:

        response = self._get().json()

        helper = ParseHelper()
        show = helper.parse_show(response[self.node][0])
        msg = helper.format_show(show)

        self.send(update, context, msg)
        return msg


class Next(Command):
    """Displays the show that comes after the current one on air."""

    def __init__(self, http_client, service_url=None, node=None):
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "live-info"
        self.node = node or "nextShow"

    def __call__(self, update, context) -> str:

        response = self._get().json()

        helper = ParseHelper()
        show = helper.parse_show(response[self.node][0])
        msg = helper.format_show(show)

        self.send(update, context, msg)
        return msg


class Today(Command):
    """Displays the radio schedule for today"""

    def __init__(self, http_client, service_url=None):
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "week-info"

    def __call__(self, update, context) -> str:
        today = dt.date.today()
        on_day = calendar.day_name[today.weekday()].lower()

        response = self._get().json()

        helper = ParseHelper()
        shows = helper.parse_shows_for_day(response, on_day)

        msg = "Shows for %s _🇩🇪 time!_\n" % (on_day.capitalize(),) + shows

        self.send(update, context, msg)
        return msg


class Tomorrow(Command):
    """Displays the radio schedule for tomorrow"""

    def __init__(self, http_client, service_url=None):
        super().__init__()
        self.http_client = http_client
        self.service_url = service_url or KEITHFEM_BASE_URL + "week-info"

    def __call__(self, update, context) -> str:
        tomorrow = dt.date.today() + dt.timedelta(days=1)

        on_day = calendar.day_name[tomorrow.weekday()].lower()

        # if tomorrow is monday, fetches 'nextmonday' on the array
        if on_day.lower() == calendar.day_name[calendar.firstweekday()].lower():
            on_day = "next" + on_day

        response = self._get().json()

        helper = ParseHelper()
        shows = helper.parse_shows_for_day(response, on_day)

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

    def __call__(self, update, context) -> str:

        response = self._get().json()

        helper = ParseHelper()

        msg = helper.parse_shows_for_week(response)

        self.send(update, context, msg)
        return msg
