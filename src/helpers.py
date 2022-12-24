import calendar
import html


class ParseHelper:
    def format_show(self, show) -> str:
        """Formats a show info to be ready to be send

        Args:
            show (tuple): ("01:00", "04:00", "name")

        Returns:
            str: a show name in bold, and start and end time. Example:
                Nocturnal Emissions (01:00 - 04:00 🇩🇪 time!)
        """
        return "*%s* (%s - %s _🇩🇪 time!_)" % (show[2:] + show[:2])

    def parse_show(self, show) -> str:
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

    def parse_shows_for_day(self, response, day) -> str:
        shows_msg = ""
        for show in response[day.lower()]:
            shows_msg += "(%s - %s) - *%s*\n" % self.parse_show(show)
        return shows_msg

    def parse_shows_for_week(self, response) -> str:
        msg = ""
        days_of_the_week = []
        for day in range(0, 7):
            days_of_the_week.append(calendar.day_name[day].lower())

        for day in response:
            if day not in days_of_the_week:
                continue
            msg += "*Shows for %s*\n" % (day.capitalize(),)
            for show in response[day]:
                msg += "(%s - %s) - *%s*\n" % self.parse_show(show)
        msg += "_ All shows are in 🇩🇪 time!_"

        return msg
