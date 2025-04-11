from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    Optional,
    List
)

from pyrogram_patch.router import Router

from app.bot.markups.text import TEXT
from app.db.db_requests import DB
from app.db.models import (
    Keywords, Keyword,
    Chats, Chat
)

if TYPE_CHECKING:
    from pyrogram.client import Client
    from pyrogram.types.messages_and_media import Message


new_message_router = Router()


@new_message_router.on_message()
async def message_handler(client: Client, message: Message):
    keywords: Optional[List[Keyword]] = await DB.get_many(
        table_cls=Keywords
    )
    chats: Optional[List[Chat]] = await DB.get_many(
        table_cls=Chats
    )
    link = message.chat.invite_link.split("/")[-1]

    if keywords and chats:
        for keyword, chat in zip(keywords, chats):
            if link in chat.link and keyword.word in message.text:
                await client.send_message(
                    chat_id=keyword.owner_id,
                    text=TEXT["message_found"].format(
                        keyword=keyword.word,
                        link=message.link
                    )
                )

                logging.info(f"Message: {message.link} parsed by keyword: {keyword.word}")  # noqa: E501


@new_message_router.on_edited_message()
async def message_edited_handler(client: Client, message: Message):
    keywords: Optional[List[Keyword]] = await DB.get_many(
        table_cls=Keywords
    )
    chats: Optional[List[Chat]] = await DB.get_many(
        table_cls=Chats
    )
    link = message.chat.invite_link.split("/")[-1]

    if keywords and chats:
        for keyword, chat in zip(keywords, chats):
            if link in chat.link and keyword.word in message.text:
                await client.send_message(
                    chat_id=keyword.owner_id,
                    text=TEXT["message_found"].format(
                        keyword=keyword.word,
                        link=message.link
                    )
                )

                logging.info(f"Message: {message.link} parsed by keyword: {keyword.word}")  # noqa: E501
