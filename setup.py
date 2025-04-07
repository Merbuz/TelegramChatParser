import logging

from pyrogram.enums.parse_mode import ParseMode

from app.bot.bot import Bot
from app.bot.handlers.message_handler import message_router
from app.bot.handlers.command_handler import command_router


bot = Bot(
    "app/bot/bot",
    parse_mode=ParseMode.MARKDOWN
)


def setup():
    # | Setting up logging

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('last_logs.log', mode='w')
    file_handler.setFormatter(
        logging.Formatter('"%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"')  # noqa: E501
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('"%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"')  # noqa: E501
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # | Include routers

    bot.include_routers(
        command_router,
        message_router
    )


def main():
    setup()

    bot.run()
