import asyncio
import logging

from pyrogram.enums.parse_mode import ParseMode
from pyrogram_patch.fsm.storages import MemoryStorage

from app.bot.bot import Bot
from app.bot.handlers.states_handler import states_router
from app.bot.handlers.command_handler import command_router
from app.bot.handlers.message_handler import message_router
from app.bot.handlers.callback_handler import callback_router
from app.settings.configparse import Settings
from app.db.db_requests import DB
from app.db.models import (
    Keyword, Keywords,
    PublicChat, PublicChats,
    PrivateChat, PrivateChats
)


bot = Bot.from_env(
    name="app/bot/session/bot",
    parse_mode=ParseMode.MARKDOWN
)


async def setup():
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

    if Settings().view_logs:
        logger.addHandler(console_handler)

    bot.set_storage(MemoryStorage())

    bot.include_routers(
        states_router,
        callback_router,
        command_router,
        message_router
    )

    await DB.create_table(
        table_cls=Keywords,
        columns="""
            word TEXT PRIMARY KEY NOT NULL,
            owner_id INT NOT NULL,
            enabled BOOLEAN DEFAULT(TRUE) NOT NULL
        """,
        table_cls_row=Keyword
    )

    await DB.create_table(
        table_cls=PublicChats,
        columns="""
            id INT PRIMARY KEY NOT NULL,
            status TEXT DEFAULT('ChatMemberStatus.LEFT')
        """,
        table_cls_row=PublicChat
    )

    await DB.create_table(
        table_cls=PrivateChats,
        columns="""
            id INT PRIMARY KEY NOT NULL,
            status TEXT DEFAULT('ChatMemberStatus.LEFT')
        """,
        table_cls_row=PrivateChat
    )


def main():
    loop = asyncio.get_event_loop()

    loop.run_until_complete(setup())
    bot.run()
