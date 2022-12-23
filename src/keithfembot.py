import logging

from telegram.ext import CommandHandler, Updater

from clients.http import HTTPClient
from commands import (About, Command, Donate, Help, Joke, Next, Now, Today,
                      Tomorrow, Week)
from config import HTTP_API_TOKEN
from exceptions import HTTPError, KeithFemException

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def error_handler(update, context) -> None:
    """Log Errors"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main(http_client=None) -> None:
    """Starts the bot."""
    updater = Updater(token=HTTP_API_TOKEN, use_context=True)

    dp = updater.dispatcher

    http_client = http_client or HTTPClient()

    try:
        dp.add_handler(CommandHandler("about", About()))
        dp.add_handler(CommandHandler("help", Help()))
        dp.add_handler(CommandHandler("joke", Joke(http_client)))
        dp.add_handler(CommandHandler("donate", Donate()))
        dp.add_handler(CommandHandler("now", Now(http_client)))
        dp.add_handler(CommandHandler("next", Next(http_client)))
        dp.add_handler(CommandHandler("today", Today(http_client)))
        dp.add_handler(CommandHandler("tomorrow", Tomorrow(http_client)))
        dp.add_handler(CommandHandler("week", Week(http_client)))

        dp.add_error_handler(error_handler)

        updater.start_polling()
        updater.idle()

    except HTTPError:
        Command.send("Looks like the Bot cannot find what you need 😪")

    except KeithFemException:
        Command.send("Nothing to say about that 🤐")
        pass


if __name__ == "__main__":
    main()
