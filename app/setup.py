import logging

from pyrogram.enums.parse_mode import ParseMode
from pyrogram_patch.fsm.storages import MemoryStorage

from app.bot.bot import Bot
from app.bot.handlers.command_handler import command_router
from app.bot.handlers.message_handler import message_router


bot = Bot.from_env(
    name="app/bot/session/bot",
    parse_mode=ParseMode.MARKDOWN
)


def setup():
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

    bot.set_storage(MemoryStorage())

    bot.include_routers(
        command_router,
        message_router
    )


def main():
    setup()

    bot.run()
