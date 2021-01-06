from unittest.mock import patch

from freezegun import freeze_time

from keithfembot import KeithFemBotCommands

""" Methods without external dependencies """


def test_about():

    msg = (
        "Keith F'em, a community radio experiment, is presented by Keith "
        "in conjuction with SP2. `hello@keithfem.com`\n"
        "Bot created in Barcelona during the COVID-19 outbreak quarantine "
        "(March 2020) ✌"
    )

    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        KFBC = KeithFemBotCommands()
        KFBC.about(update=None, context=None)
        mock_send.assert_called_once_with(None, None, msg)


def test_donate():

    msg = "[https://www.paypal.me/keithfem]"

    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        KFBC = KeithFemBotCommands()
        KFBC.donate(update=None, context=None)
        mock_send.assert_called_once_with(None, None, msg)


def test_togo():

    msg = (
        "Keith Togo 🇹🇬\n"
        "Thursday - Sunday 15-20h\n"
        "Check https://t.me/keithtogo for more details\n"
    )

    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        KFBC = KeithFemBotCommands()
        KFBC.togo(update=None, context=None)
        mock_send.assert_called_once_with(None, None, msg)


def test_help():

    msg = (
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

    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        KFBC = KeithFemBotCommands()
        KFBC.help(update=None, context=None)
        mock_send.assert_called_once_with(None, None, msg)


""" Methods with external dependencies """


def test_joke():
    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        with patch("requests.get") as patched_get:
            KFBC = KeithFemBotCommands()
            KFBC.joke(update=None, context=None)
            patched_get.assert_called_once()
            mock_send.assert_called_once()


def test_gibberish():
    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        with patch("requests.get") as patched_get:
            KFBC = KeithFemBotCommands()
            KFBC.gibberish(update=None, context=None)
            patched_get.assert_called_once()
            mock_send.assert_called_once()


def test_next(response_live_info):
    msg = "*Franky Teardrop's Post-Victorian Classical* (22:00 - 00:00 _🇩🇪 time!_)"

    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        with patch("requests.get") as patched_get:
            patched_get.return_value = response_live_info
            KFBC = KeithFemBotCommands()
            KFBC.next(update=None, context=None)

            patched_get.assert_called_once()
            mock_send.assert_called_once_with(None, None, msg)


def test_now(response_live_info):
    msg = "*Keith F'em Bot DJ* (20:00 - 22:00 _🇩🇪 time!_)"

    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        with patch("requests.get") as patched_get:
            patched_get.return_value = response_live_info
            KFBC = KeithFemBotCommands()
            KFBC.now(update=None, context=None)

            patched_get.assert_called_once()
            mock_send.assert_called_once_with(None, None, msg)


@freeze_time("2020-12-29")  # Wednesday
def test_tomorrow(response_week_info):
    msg = (
        "Shows for Wednesday _🇩🇪 time!_\n"
        "(00:00 - 02:00) - *DJ MFK - Best of the 20Tens*\n"
        "(02:00 - 04:00) - *El Melómano Alemán Revisit*\n"
        "(04:00 - 06:00) - *Still Hating Revisited*\n"
        "(11:00 - 13:00) - *Misunderestimated*\n"
        "(13:00 - 15:00) - *Actual Figures*\n"
        "(15:00 - 16:00) - *The Keith Family Punk Hour*\n"
        "(16:00 - 18:00) - *Ambient Music Service for Sleepwaking*\n"
        "(18:00 - 20:00) - *Kraut Kontrol*\n"
        "(20:00 - 23:00) - *The Broth*\n"
        "(23:00 - 01:00) - *The Boring Music Show*\n"
    )
    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        with patch("requests.get") as patched_get:
            patched_get.return_value = response_week_info
            KFBC = KeithFemBotCommands()
            KFBC.tomorrow(update=None, context=None)

            patched_get.assert_called_once()
            mock_send.assert_called_once_with(None, None, msg)


@freeze_time("2020-12-29")  # Tuesday
def test_today(response_week_info):
    msg = (
        "Shows for Tuesday _🇩🇪 time!_\n"
        "(00:00 - 01:00) - *Keith F'em Bot DJ*\n"
        "(01:00 - 02:00) - *The Matinee Radio Show Revisit*\n"
        "(02:00 - 04:00) - *Keith F'em Bot DJ*\n"
        "(04:00 - 06:00) - *Window Magic's Transmission Service*\n"
        "(06:00 - 08:00) - *Franktankerous' Psychedelic Extravaganza Revisited*\n"
        "(08:00 - 11:00) - *Last Week's Broth*\n"
        "(11:00 - 13:00) - *Kraut Kontrol Revisited*\n"
        "(13:00 - 14:00) - *The Keith Family Metal Hour*\n"
        "(14:00 - 20:00) - *Keith F'em Bot DJ*\n"
        "(20:00 - 22:00) - *Hardcore Tuesdays*\n"
    )

    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        with patch("requests.get") as patched_get:
            patched_get.return_value = response_week_info
            KFBC = KeithFemBotCommands()
            KFBC.today(update=None, context=None)

            patched_get.assert_called_once()
            mock_send.assert_called_once_with(None, None, msg)


@freeze_time("2020-12-29")
def test_week(response_week_info):
    msg = (
        "*Shows for Monday*\n"
        "(00:00 - 08:00) - *Keith F'em Bot DJ*\n"
        "(08:00 - 09:00) - *Keith F'em Bot DJ*\n"
        "(09:00 - 11:00) - *Caprisonne Revisited*\n"
        "(11:00 - 13:00) - *Keith F'em Bot DJ*\n"
        "(13:00 - 14:00) - *The Keith Family ExperimentalHour*\n"
        "(14:00 - 16:00) - *Keith F'em Bot DJ*\n"
        "(16:00 - 18:00) - *Liv and Ken play Heavy Rock for Moms*\n"
        "(18:00 - 20:00) - *Still Hating*\n"
        "(20:00 - 21:00) - *wood, metal, stoned*\n"
        "(21:00 - 22:00) - *Ängstkiste*\n"
        "(22:00 - 00:00) - *Novo line*\n"
        "*Shows for Tuesday*\n"
        "(00:00 - 01:00) - *Keith F'em Bot DJ*\n"
        "(01:00 - 02:00) - *The Matinee Radio Show Revisit*\n"
        "(02:00 - 04:00) - *Keith F'em Bot DJ*\n"
        "(04:00 - 06:00) - *Window Magic's Transmission Service*\n"
        "(06:00 - 08:00) - *Franktankerous' Psychedelic Extravaganza Revisited*\n"
        "(08:00 - 11:00) - *Last Week's Broth*\n"
        "(11:00 - 13:00) - *Kraut Kontrol Revisited*\n"
        "(13:00 - 14:00) - *The Keith Family Metal Hour*\n"
        "(14:00 - 20:00) - *Keith F'em Bot DJ*\n"
        "(20:00 - 22:00) - *Hardcore Tuesdays*\n"
        "*Shows for Wednesday*\n"
        "(00:00 - 02:00) - *DJ MFK - Best of the 20Tens*\n"
        "(02:00 - 04:00) - *El Melómano Alemán Revisit*\n"
        "(04:00 - 06:00) - *Still Hating Revisited*\n"
        "(11:00 - 13:00) - *Misunderestimated*\n"
        "(13:00 - 15:00) - *Actual Figures*\n"
        "(15:00 - 16:00) - *The Keith Family Punk Hour*\n"
        "(16:00 - 18:00) - *Ambient Music Service for Sleepwaking*\n"
        "(18:00 - 20:00) - *Kraut Kontrol*\n"
        "(20:00 - 23:00) - *The Broth*\n"
        "(23:00 - 01:00) - *The Boring Music Show*\n"
        "*Shows for Thursday*\n"
        "(01:00 - 02:00) - *The Matinee Radio Show Revisit*\n"
        "(02:00 - 04:00) - *Franky Teardrop's Post-Victorian Classical Revisited*\n"
        "(04:00 - 06:00) - *Caprisonne Revisited*\n"
        "(08:00 - 10:00) - *Randy's Roadhouse Revisited*\n"
        "(13:00 - 15:00) - *Snake Jazz*\n"
        "(16:00 - 17:00) - *The Keith Family Indie Rock Hour*\n"
        "(17:00 - 18:00) - *Talk To Me*\n"
        "(20:00 - 22:00) - *The Pinnacle*\n"
        "(22:00 - 02:00) - *Best of IntergalacticFM New Years Special 2021*\n"
        "*Shows for Friday*\n"
        "(02:00 - 03:00) - *Memory Foam with DJ Your Body*\n"
        "(04:00 - 06:00) - *Still Hating Revisited*\n"
        "(06:00 - 08:00) - *Faintfest Revisited*\n"
        "(11:00 - 13:00) - *Misunderestimated*\n"
        "(13:00 - 14:00) - *The Keith Family Blues Hour*\n"
        "(14:00 - 16:00) - *Window Magic's Transmission Service*\n"
        "(16:00 - 18:00) - *Slow Rise Radio*\n"
        "(18:00 - 20:00) - *Sausage Man Radio*\n"
        "(20:00 - 22:00) - *Randy's Roadhouse*\n"
        "*Shows for Saturday*\n"
        "(06:00 - 08:00) - *The Boring Music Show Revisit*\n"
        "(08:00 - 10:00) - *Kraut Kontrol Revisited*\n"
        "(10:00 - 12:00) - *The Cunning Ape*\n"
        "(12:00 - 14:00) - *Misunderestimated*\n"
        "(14:00 - 16:00) - *Snake Jazz Replay Saturday*\n"
        "(20:00 - 22:00) - *Franktankerous's Psychedelic Extravaganza*\n"
        "(22:00 - 00:00) - *Faintfest*\n"
        "*Shows for Sunday*\n"
        "(00:00 - 02:00) - *Hardcore Tuesday Revisits*\n"
        "(02:00 - 04:00) - *Liv Me Alone Revisited*\n"
        "(06:00 - 09:00) - *Ambiencia Maximatosis*\n"
        "(14:00 - 16:00) - *El Melómano Alemán*\n"
        "(16:00 - 18:00) - *Fuddle Duddle with DJ the Duncan*\n"
        "(18:00 - 20:00) - *Ok, let's do it!*\n"
        "(20:00 - 22:00) - *Keith Femme*\n"
        "(22:00 - 00:00) - *Franky Teardrop's Post-Victorian Classical*\n"
        "_ All shows are in 🇩🇪 time!_"
    )
    with patch.object(KeithFemBotCommands, "_send", return_value=None) as mock_send:
        with patch("requests.get") as patched_get:
            patched_get.return_value = response_week_info
            KFBC = KeithFemBotCommands()
            KFBC.week(update=None, context=None)

            patched_get.assert_called_once()
            mock_send.assert_called_once_with(None, None, msg)
