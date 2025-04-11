from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    List
)

from pyrogram import filters
from pyrogram_patch.router import Router
from pyrogram_patch.fsm import State
from pyrogram_patch.fsm.filter import StateFilter

from app.bot.states.group import ActionStates
from app.bot.markups.inline_markups import InlineKeyboardMenus
from app.bot.markups.text import TEXT
from app.db.db_requests import DB
from app.db.models import (
    Keywords, Keyword,
    PublicChats, PublicChat,
    PrivateChats, PrivateChat
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
