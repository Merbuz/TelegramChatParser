from __future__ import annotations

from typing import (
    TYPE_CHECKING
)

from pyrogram.enums import ChatType
from pyrogram_patch.fsm import State
from pyrogram_patch.router import Router
from pyrogram_patch.fsm.filter import StateFilter
from pyrogram.errors.exceptions.bad_request_400 import BotMethodInvalid

from app.bot.states.group import ActionStates
from app.bot.markups.inline_markups import InlineKeyboardMenus
from app.bot.markups.text import TEXT
from app.db.db_requests import DB
from app.db.models import (
    Keywords,
    Chats
)

if TYPE_CHECKING:
    from pyrogram.client import Client
    from pyrogram.types.messages_and_media import Message


states_router = Router()


@states_router.on_message(
    StateFilter(ActionStates.add_keyword)  # type: ignore
)
async def add_keyword(client: Client, message: Message, state: State):
    if len(message.text) <= 50:
        await DB.add(
            table_cls=Keywords,
            sql_args=[
                "word",
                "owner_id",
                "enabled"
            ],
            sql_values=[
                message.text,
                message.from_user.id,
                True
            ]
        )

        await message.reply(
            text=TEXT["keyword_added"],
            reply_markup=await InlineKeyboardMenus.back("manage_keywords")
        )

        await state.finish()

    else:
        await message.reply(
            text=TEXT["add_keyword"],
            reply_markup=await InlineKeyboardMenus.back("manage_keywords")
        )


@states_router.on_message(
    StateFilter(ActionStates.add_chat)  # type: ignore
)
async def add_chat(client: Client, message: Message, state: State):
    try:
        chat = await client.get_chat(message.text)

        if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
            await DB.add(
                table_cls=Chats,
                sql_args=[
                    "link",
                    "id"
                ],
                sql_values=[
                    chat.username,
                    chat.id
                ]
            )

            await message.reply(
                text=TEXT["link_added"],
                reply_markup=await InlineKeyboardMenus.back("manage_links")
            )

            await state.finish()

        else:
            await message.reply(
                text=TEXT["add_link"],
                reply_markup=await InlineKeyboardMenus.back("manage_links")
            )

    except BotMethodInvalid:
        await DB.add(
            table_cls=Chats,
            sql_args=[
                "link"
            ],
            sql_values=[
                message.text.split("/")[-1]
            ]
        )

        await message.reply(
            text=TEXT["link_added"],
            reply_markup=await InlineKeyboardMenus.back("manage_links")
        )

        await state.finish()

    except Exception:
        await message.reply(
            text=TEXT["add_link"],
            reply_markup=await InlineKeyboardMenus.back("manage_links")
        )


@states_router.on_message(
    StateFilter(ActionStates.add_session)  # type: ignore
)
async def add_session(client: Client, message: Message, state: State):
    if message.document and message.document.file_name.endswith(".session"):
        await message.download(
            file_name=f"./sessions/{message.document.file_name}"
        )

        await message.reply(
            text=TEXT["session_added"],
            reply_markup=await InlineKeyboardMenus.back("manage_sessions")
        )

        await state.finish()

    else:
        await message.reply(
            text=TEXT["add_session"],
            reply_markup=await InlineKeyboardMenus.back("manage_sessions")
        )
