from keithfembot import KeithFemBotCommands


def test_parse_show(show):
    KFBC = KeithFemBotCommands()
    (starts, ends, name) = KFBC._parse_show(show)

    assert starts == "00:00"
    assert ends == "02:00"
    assert name == "Hardcore Tuesday Revisits"


def test_parse_show_special_chars(show):
    KFBC = KeithFemBotCommands()
    show["name"] = show["name"] + "*!"
    (starts, ends, name) = KFBC._parse_show(show)

    assert starts == "00:00"
    assert ends == "02:00"
    assert name == "Hardcore Tuesday Revisits\\*\\!"
