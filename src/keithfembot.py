import logging
import os
import time

from telegram.ext import CallbackContext, CommandHandler, Updater

from clients.http import HTTPClient
from commands import About, Donate, Help, Joke, Next, Now, Today, Tomorrow, Week
from config import HTTP_API_TOKEN, TIMEZONE

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    message = "Looks like the Bot cannot find what you need 😪"
    context.bot.send_message(update, context, message)


def main(http_client=None) -> None:
    """Starts the bot."""

    os.environ["TZ"] = TIMEZONE
    time.tzset()  # Unix only function

    updater = Updater(token=HTTP_API_TOKEN, use_context=True)

    dp = updater.dispatcher  # type: ignore

    http_client = http_client or HTTPClient()

    dp.add_handler(CommandHandler("about", About()))  # type: ignore
    dp.add_handler(CommandHandler("help", Help()))  # type: ignore
    dp.add_handler(CommandHandler("joke", Joke(http_client)))  # type: ignore
    dp.add_handler(CommandHandler("donate", Donate()))  # type: ignore
    dp.add_handler(CommandHandler("now", Now(http_client)))  # type: ignore
    dp.add_handler(CommandHandler("next", Next(http_client)))  # type: ignore
    dp.add_handler(CommandHandler("today", Today(http_client)))  # type: ignore
    dp.add_handler(CommandHandler("tomorrow", Tomorrow(http_client)))  # type: ignore
    dp.add_handler(CommandHandler("week", Week(http_client)))  # type: ignore

    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
