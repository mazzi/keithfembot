from unittest.mock import patch

import pytest
import requests
from freezegun import freeze_time

from clients.fakes.http import FakeHTTPClient
from commands import (
    About,
    Command,
    Donate,
    Help,
    Joke,
    Next,
    Now,
    Today,
    Tomorrow,
    Week,
)
from exceptions import HTTPError


class TestCommandsWithoutDependencies:
    """Methods without external dependencies"""

    def test_about(self, about) -> None:

        with patch.object(Command, "send", return_value=None) as mock_send:
            result = About()(update=None, context=None)
            mock_send.assert_called_once_with(None, None, about)

        assert result == about

    def test_donate(self, donate) -> None:

        with patch.object(Command, "send", return_value=None) as mock_send:
            result = Donate()(update=None, context=None)
            mock_send.assert_called_once_with(None, None, donate)

        assert result == donate

    def test_help(self, help):

        with patch.object(Command, "send", return_value=None) as mock_send:
            result = Help()(update=None, context=None)
            mock_send.assert_called_once_with(None, None, help)

        assert result == help


class TestCommandsWithDependencies:
    """Methods with external dependencies"""

    def test_joke(self, joke):

        expected_joke = joke

        with patch.object(Command, "send", return_value=None) as mock_send:
            result = Joke(FakeHTTPClient())(update=None, context=None)
            mock_send.assert_called_once()

        assert result == expected_joke

    def test_joke_fails_without_header(self):

        with pytest.raises(HTTPError) as e:
            with patch.object(Command, "send", return_value=None) as mock_send:
                Joke(FakeHTTPClient(), headers={"bad": "header"})(
                    update=None, context=None
                )
                mock_send.assert_called_once()

        assert "User-Agent and Accept is needed for this service." in str(e.value)

    @freeze_time("2020-12-27")  # Sunday
    def test_now(self, response_live_info):
        expected_show = "*Keith F'em Bot DJ* (20:00 - 22:00 _🇩🇪 time!_)"
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_live_info
                msg = Now(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected_show

    @freeze_time("2020-12-29")  # Tuesday
    def test_now_is_empty(self, response_live_info_with_empty_shows):
        expected_show = (
            "Nothing being broadcasted at the moment 🥺.\n"
            "Check the weekly schedule with /week command."
        )
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_live_info_with_empty_shows
                msg = Now(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected_show

    @freeze_time("2020-12-27")  # Sunday
    def test_next(self, response_live_info):
        expected_show = (
            "*Franky Teardrop's Post-Victorian Classical* (22:00 - 00:00 _🇩🇪 time!_)"
        )
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_live_info
                msg = Next(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected_show

    @freeze_time("2020-12-29")  # Tuesday
    def test_next_is_tomorrow(self, response_live_info_with_empty_shows):
        expected_show = "*Actual Figures* (15:00 - 17:00 _🇩🇪 time!_)"
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_live_info_with_empty_shows
                msg = Next(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected_show

    @freeze_time("2020-12-28")  # Monday
    def test_next_is_empty(self, response_live_info_with_empty_shows):
        expected_show = (
            "Nothing else scheduled for today 🥺.\n"
            "Check the weekly schedule with /week command."
        )
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_live_info_with_empty_shows
                msg = Next(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected_show

    @freeze_time("2020-12-29")  # Tuesday
    def test_today(self, response_week_info):
        expected = (
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
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_week_info
                msg = Today(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected

    @freeze_time("2020-12-29")  # Tuesday
    def test_today_is_empty(self, response_week_info_with_empty_days):
        expected = (
            "No shows are scheduled for today 🤷.\n"
            "Check the weekly schedule with /week command."
        )
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_week_info_with_empty_days
                msg = Today(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected

    @freeze_time("2020-12-29")  # Tuesday
    def test_tomorrow(self, response_week_info):
        expected = (
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
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_week_info
                msg = Tomorrow(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected

    @freeze_time("2020-12-28")  # Monday
    def test_tomorrow_is_empty(self, response_week_info_with_empty_days):
        expected = (
            "No shows are scheduled for tomorrow 🤷.\n"
            "Check the weekly schedule with /week command."
        )
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_week_info_with_empty_days
                msg = Tomorrow(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected

    @freeze_time("2020-12-27")  # Sunday
    def test_tomorrow_when_sunday(self, response_week_info):
        expected = (
            "Shows for Monday _🇩🇪 time!_\n"
            "(02:00 - 04:00) - *The Cunning Ape Revisited*\n"
            "(13:00 - 14:00) - *The Keith Family ExperimentalHour*\n"
            "(15:00 - 16:00) - *Art Next Door*\n"
            "(18:00 - 20:00) - *Still Hating*\n"
            "(20:00 - 22:00) - *Ängstkiste*\n"
        )
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_week_info
                msg = Tomorrow(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected

    @freeze_time("2020-12-29")  # Wednesday
    def test_week(self, response_week_info):
        expected = (
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
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_week_info
                msg = Week(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected

    @freeze_time("2020-12-29")  # Wednesday
    def test_week_with_empty_days(self, response_week_info_with_empty_days):
        expected = (
            "*Shows for Wednesday*\n"
            "(15:00 - 17:00) - *Actual Figures*\n"
            "(18:00 - 20:00) - *Kraut Kontrol*\n"
            "(20:00 - 23:00) - *The Broth*\n"
            "(23:00 - 23:25) - *Hearse Case Scenario - Die Bestatterinnen*\n"
            "*Shows for Thursday*\n"
            "(18:00 - 19:00) - *Arbitrarily Deterministic*\n"
            "(22:00 - 00:00) - *Kujiradio*\n"
            "*Shows for Friday*\n"
            "(18:00 - 20:00) - *Sentient Hairstyles*\n"
            "(20:00 - 21:15) - *Blauer Planet*\n"
            "*Shows for Saturday*\n"
            "(19:00 - 20:00) - *Angstkiste*\n"
            "*Shows for Sunday*\n"
            "(10:00 - 12:00) - *Steve’s Radio Show*\n"
            "(12:00 - 12:50) - *Red Transmissions*\n"
            "(16:00 - 18:00) - *Fuddle Duddle with DJ the Duncan & DinosaurOskar*\n"
            "_ All shows are in 🇩🇪 time!_"
        )
        with patch.object(Command, "send", return_value=None) as mock_send:
            with patch("requests.get") as patched_get:
                patched_get.return_value = response_week_info_with_empty_days
                msg = Week(http_client=requests)(update=None, context=None)

                patched_get.assert_called_once()
                mock_send.assert_called_once_with(None, None, msg)

        assert msg == expected
