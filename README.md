[![Coverage Status](https://coveralls.io/repos/github/mazzi/keithfembot/badge.svg?branch=main)](https://coveralls.io/github/mazzi/keithfembot?branch=main)

# Keithfem Bot
A Telegram bot for [www.keithfem.com](https://www.keithfem.com/) that displays the radio shows schedule.

<img src="https://user-images.githubusercontent.com/121728/206558417-2ce25cec-53f7-480a-82a7-8637dc77f555.jpeg" width="225" alt="KeithfemBotMeister Logo" />

## Commands
* `/now` : displays the show that is on air at the moment.
* `/next` : displays the upcoming show.
* `/today`: displays the schedule for today.
* `/tomorrow`: displays the schedule for tomorrow.
* `/week`: displays the shows for the week.
* `/gibberish`: some gibberish.
* `/about`: the usual stuff that an about command displays.
* `/joke`: KeithF'em BotMeister, tell me a joke
* `/donate`: donate to Keith F'em.
* `/help`: help about the commands.

## Config
Create a .envrc with these environment variables. Use [direnv](https://direnv.net/).

```
export PYTHONPATH=./src/
export KEITHFEM_BASE_URL=
export HTTP_API_TOKEN=
export FORTUNE_URL=https://anothervps.com/api/fortune/
export DADJOKE_URL=https://icanhazdadjoke.com/
```

KEITHFEM_BASE_URL is the [airtime](https://www.airtime.pro/) base url of the radio.

HTTP_API_TOKEN is from [@Botfather](https://web.telegram.org/#/im?p=@BotFather)

FORTUNE_URL is a fortunes service.

DADJOKE_URL is a jokes service.


<sub><sup>Keith F'em, a community radio experiment, is presented by Keith in conjunction with SP2. hello@keithfem.com</sup></sub>
