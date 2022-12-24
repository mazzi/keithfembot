import pytest

from helpers import ParseHelper


class TestHelpers:

    @pytest.mark.parametrize("tuple, expected", [
        (("01:00", "04:00", "Nocturnal Emissions"),
         "*Nocturnal Emissions* (01:00 - 04:00 _🇩🇪 time!_)"),
    ])
    def test_format_show(self, tuple, expected) -> None:
        helper = ParseHelper()
        result = helper.format_show(tuple)
        assert result == expected

    @pytest.mark.parametrize("dictionary, expected", [
        ({
            "name": "Nocturnal Emissions",
            "starts": "2020-12-23 01:00:00",
            "ends": "2020-12-23 04:00:00",
         },
         ("01:00", "04:00", "Nocturnal Emissions")),
    ])  # TODO: More cases with the dict: missing keys; wrong info.
    def test_parse_show(self, dictionary, expected) -> None:
        helper = ParseHelper()
        result = helper.parse_show(dictionary)
        assert result == expected

    def test_parse_shows_for_day(self, response_week_info) -> None:
        expected = (
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
        helper = ParseHelper()
        result = helper.parse_shows_for_day(response_week_info.json(), "wednesday")
        assert result == expected

    def test_parse_shows_for_week(self, response_week_info) -> None:
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
        helper = ParseHelper()
        result = helper.parse_shows_for_week(response_week_info.json())
        assert result == expected
