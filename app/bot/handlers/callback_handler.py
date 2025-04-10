from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram_patch.router import Router
from pyrogram_patch.fsm import State
from pyrogram_patch.fsm.filter import StateFilter

from app.bot.states.group import ActionStates
from app.bot.callback_query.filter import CallbackFilter
from app.bot.markups.inline_markups import InlineKeyboardMenus
from app.bot.markups.text import TEXT
from app.db.db_requests import DB
from app.db.models import (
    Keywords
)


if TYPE_CHECKING:
    from pyrogram.client import Client
    from pyrogram.types import CallbackQuery


callback_router = Router()


@callback_router.on_callback_query(CallbackFilter.filter("start"))
async def start(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        text=TEXT["start"],
        reply_markup=await InlineKeyboardMenus.start()
    )


@callback_router.on_callback_query(CallbackFilter.filter("manage_keywords"))
async def manage_keywords(client: Client, query: CallbackQuery, state: State):
    await query.message.edit_text(
        text=TEXT["choose_action"],
        reply_markup=await InlineKeyboardMenus.manage_keywords()
    )
    await state.finish()


@callback_router.on_callback_query(CallbackFilter.filter("add_keyword"))
async def add_keyword(client: Client, query: CallbackQuery, state: State):
    await query.message.edit_text(
        text=TEXT["add_keyword"],
        reply_markup=await InlineKeyboardMenus.back("manage_keywords")
    )
    await state.set_state(ActionStates.add_keyword)


@callback_router.on_callback_query(CallbackFilter.filter("keywords_list"))
async def keywords_list(client: Client, query: CallbackQuery):
    keywords = await DB.get_many(
        table_cls=Keywords,
        sql_args=[
            "owner_id"
        ],
        sql_values=[
            query.from_user.id
        ]
    )

    await query.message.edit_text(
        text=TEXT["keywords_list"] if keywords else TEXT["keywords_not_found"],
        reply_markup=await InlineKeyboardMenus.keywords_list(
            owner_id=query.from_user.id
        )
    )
