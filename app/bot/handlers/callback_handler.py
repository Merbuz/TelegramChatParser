from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Optional,
    List
)
from pathlib import Path

from pyrogram_patch.router import Router
from pyrogram_patch.fsm import State

from app.bot.states.group import ActionStates
from app.bot.callback_query.filter import CallbackFilter
from app.bot.markups.inline_markups import InlineKeyboardMenus
from app.bot.markups.text import TEXT
from app.db.db_requests import DB
from app.db.models import (
    Keywords, Keyword,
    Chats, Chat
)
from app.bot.callback_query.callback_data import (
    KeywordData,
    KeywordParse,
    KeywordRemove,
    ChatData,
    ChatRemove,
    SessionData,
    SessionRemove
)
from app.parser.botnet import Parser

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
    parser = Parser()

    if not parser.parsing:
        await query.message.edit_text(
            text=TEXT["add_keyword"],
            reply_markup=await InlineKeyboardMenus.back("manage_keywords")
        )
        await state.set_state(ActionStates.add_keyword)

    else:
        await query.message.edit_text(
            text=TEXT["disable_parsing"],
            reply_markup=await InlineKeyboardMenus.back(
                data="manage_keywords"
            )
        )


@callback_router.on_callback_query(CallbackFilter.filter("keywords_list"))
async def keywords_list(client: Client, query: CallbackQuery):
    keywords: Optional[List[Keyword]] = await DB.get_many(
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
    parser = Parser()

    if not parser.parsing:
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

    else:
        await query.message.edit_text(
            text=TEXT["disable_parsing"],
            reply_markup=await InlineKeyboardMenus.back(
                data="manage_keywords"
            )
        )


@callback_router.on_callback_query(CallbackFilter.filter("manage_links"))
async def manage_links(client: Client, query: CallbackQuery, state: State):  # noqa: E501
    await query.message.edit_text(
        text=TEXT["choose_action"],
        reply_markup=await InlineKeyboardMenus.manage_links()
    )
    await state.finish()


@callback_router.on_callback_query(CallbackFilter.filter("add_link"))
async def add_link(client: Client, query: CallbackQuery, state: State):
    parser = Parser()

    if not parser.parsing:
        await query.message.edit_text(
            text=TEXT["add_link"],
            reply_markup=await InlineKeyboardMenus.back("manage_links")
        )
        await state.set_state(ActionStates.add_chat)

    else:
        await query.message.edit_text(
            text=TEXT["disable_parsing"],
            reply_markup=await InlineKeyboardMenus.back(
                data="manage_links"
            )
        )


@callback_router.on_callback_query(CallbackFilter.filter("links_list"))
async def links_list(client: Client, query: CallbackQuery):
    links: Optional[List[Chat]] = await DB.get_many(
        table_cls=Chats
    )

    await query.message.edit_text(
        text=TEXT["links_list" if links else "links_not_found"],
        reply_markup=await InlineKeyboardMenus.links_list()
    )


@callback_router.on_callback_query(ChatData.filter())
async def manage_link(client: Client, query: CallbackQuery):
    callback_data = ChatData.unpack(query.data)

    chat: Optional[Chat] = await DB.get(
        table_cls=Chats,
        sql_args=[
            "link"
        ],
        sql_values=[
            callback_data.link
        ]
    )

    await query.message.edit_text(
        text=TEXT["choose_action" if chat else "link_not_found"],
        reply_markup=await InlineKeyboardMenus.manage_link(
            link=callback_data.link
        )
    )


@callback_router.on_callback_query(ChatRemove.filter())
async def remove_link(client: Client, query: CallbackQuery):
    callback_data = ChatRemove.unpack(query.data)
    parser = Parser()

    if not parser.parsing:
        await DB.remove(
            table_cls=Chats,
            sql_args=[
                "link"
            ],
            sql_values=[
                callback_data.link
            ]
        )

        await query.message.edit_text(
            text=TEXT["link_removed"],
            reply_markup=await InlineKeyboardMenus.back(
                data="manage_links"
            )
        )

    else:
        await query.message.edit_text(
            text=TEXT["disable_parsing"],
            reply_markup=await InlineKeyboardMenus.back(
                data="manage_links"
            )
        )


@callback_router.on_callback_query(CallbackFilter.filter("manage_sessions"))
async def manage_sessions(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        text=TEXT["choose_action"],
        reply_markup=await InlineKeyboardMenus.manage_sessions()
    )


@callback_router.on_callback_query(CallbackFilter.filter("add_session"))
async def add_session(client: Client, query: CallbackQuery, state: State):
    parser = Parser()

    if not parser.parsing:
        await query.message.edit_text(
            text=TEXT["add_session"],
            reply_markup=await InlineKeyboardMenus.back("manage_sessions")
        )
        await state.set_state(ActionStates.add_session)

    else:
        await query.message.edit_text(
            text=TEXT["disable_parsing"],
            reply_markup=await InlineKeyboardMenus.back(
                data="manage_sessions"
            )
        )


@callback_router.on_callback_query(CallbackFilter.filter("sessions_list"))
async def sessions_list(client: Client, query: CallbackQuery):
    sessions = [session for session in Path("./sessions").glob("*.session")]

    await query.message.edit_text(
        text=TEXT["sessions_list" if sessions else "sessions_not_found"],
        reply_markup=await InlineKeyboardMenus.sessions_list()
    )


@callback_router.on_callback_query(SessionData.filter())
async def manage_session(client: Client, query: CallbackQuery):
    callback_data = SessionData.unpack(query.data)
    session = Path(f"./sessions/{callback_data.name}")

    await query.message.edit_text(
        text=TEXT["choose_action" if session.exists() else "session_not_found"],  # noqa: E501
        reply_markup=await InlineKeyboardMenus.manage_session(
            name=callback_data.name
        )
    )


@callback_router.on_callback_query(SessionRemove.filter())
async def remove_session(client: Client, query: CallbackQuery):
    callback_data = SessionRemove.unpack(query.data)
    session = Path(f"./sessions/{callback_data.name}")
    parser = Parser()

    if not parser.parsing:
        if session.exists():
            session.unlink()

        await query.message.edit_text(
            text=TEXT["session_removed"],
            reply_markup=await InlineKeyboardMenus.back(
                data="manage_sessions"
            )
        )

    else:
        await query.message.edit_text(
            text=TEXT["disable_parsing"],
            reply_markup=await InlineKeyboardMenus.back(
                data="manage_sessions"
            )
        )


@callback_router.on_callback_query(CallbackFilter.filter("manage_parser"))
async def manage_parser(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        text=TEXT["choose_action"],
        reply_markup=await InlineKeyboardMenus.manage_parser()
    )


@callback_router.on_callback_query(CallbackFilter.filter("parser_parsing"))
async def parser_parsing(client: Client, query: CallbackQuery):
    parser = Parser()

    if parser.parsing:
        await parser.stop()

    else:
        await parser.run()

    await query.message.edit_text(
        text=TEXT["choose_action"],
        reply_markup=await InlineKeyboardMenus.manage_parser()
    )
