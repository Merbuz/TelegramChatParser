from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Optional
)

from pyrogram_patch.router import Router
from pyrogram_patch.fsm import State

from app.bot.states.group import ActionStates
from app.bot.callback_query.filter import CallbackFilter
from app.bot.markups.inline_markups import InlineKeyboardMenus
from app.bot.markups.text import TEXT
from app.db.db_requests import DB
from app.db.models import (
    Keywords, Keyword,
    PublicChats, PublicChat,
    PrivateChats, PrivateChat
)
from app.bot.callback_query.callback_data import (
    KeywordData,
    KeywordParse,
    KeywordRemove
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
        text=TEXT["keywords_list" if keywords else "keywords_not_found"],
        reply_markup=await InlineKeyboardMenus.keywords_list(
            owner_id=query.from_user.id
        )
    )


@callback_router.on_callback_query(KeywordData.filter())
async def manage_keyword(client: Client, query: CallbackQuery):
    callback_data = KeywordData.unpack(query.data)

    keyword: Optional[Keyword] = await DB.get(
        table_cls=Keywords,
        sql_args=[
            "word",
            "owner_id"
        ],
        sql_values=[
            callback_data.word,
            query.from_user.id
        ]
    )

    await query.message.edit_text(
        text=TEXT["choose_action" if keyword else "keyword_not_found"],
        reply_markup=await InlineKeyboardMenus.manage_keyword(
            word=callback_data.word
        )
    )


@callback_router.on_callback_query(KeywordParse.filter())
async def parse_keyword(client: Client, query: CallbackQuery):
    callback_data = KeywordParse.unpack(query.data)

    keyword: Optional[Keyword] = await DB.get(
        table_cls=Keywords,
        sql_args=[
            "word",
            "owner_id"
        ],
        sql_values=[
            callback_data.word,
            query.from_user.id
        ]
    )

    if keyword:
        await DB.update(
            table_cls=Keywords,
            need_to_update_values=[
                "enabled"
            ],
            sql_values=[
                not keyword.enabled
            ],
            where_sql_arg="word",
            sql_arg=keyword.word
        )

    await query.message.edit_text(
        text=TEXT["choose_action" if keyword else "keyword_not_found"],
        reply_markup=await InlineKeyboardMenus.manage_keyword(
            word=callback_data.word
        )
    )


@callback_router.on_callback_query(KeywordRemove.filter())
async def remove_keyword(client: Client, query: CallbackQuery):
    callback_data = KeywordRemove.unpack(query.data)

    await DB.remove(
        table_cls=Keywords,
        sql_args=[
            "word"
        ],
        sql_values=[
            callback_data.word
        ]
    )

    await query.message.edit_text(
        text=TEXT["keyword_removed"],
        reply_markup=await InlineKeyboardMenus.back(
            data="manage_keywords"
        )
    )


@callback_router.on_callback_query(CallbackFilter.filter("manage_links"))
async def manage_links(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        text=TEXT["choose_action"],
        reply_markup=await InlineKeyboardMenus.manage_links()
    )


@callback_router.on_callback_query(CallbackFilter.filter("public_links"))
async def manage_public_links(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        text=TEXT["choose_action"],
        reply_markup=await InlineKeyboardMenus.manage_public_links()
    )


@callback_router.on_callback_query(CallbackFilter.filter("private_links"))
async def manage_private_links(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        text=TEXT["choose_action"],
        reply_markup=await InlineKeyboardMenus.manage_private_links()
    )


@callback_router.on_callback_query(CallbackFilter.filter("public_links_list"))
async def public_links_list(client: Client, query: CallbackQuery):
    links = await DB.get_many(
        table_cls=PublicChats
    )

    await query.message.edit_text(
        text=TEXT["links_list" if links else "links_not_found"],
        reply_markup=await InlineKeyboardMenus.public_links_list()
    )


@callback_router.on_callback_query(CallbackFilter.filter("private_links_list"))
async def private_links_list(client: Client, query: CallbackQuery):
    links = await DB.get_many(
        table_cls=PrivateChats
    )

    await query.message.edit_text(
        text=TEXT["links_list" if links else "links_not_found"],
        reply_markup=await InlineKeyboardMenus.private_links_list()
    )
