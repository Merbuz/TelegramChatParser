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

    if chats and keywords:
        db_chats = []
        enabled_keywords = [keyword for keyword in keywords if keyword.enabled]

        for chat in chats:
            try:
                db_chats.append(
                    (await client.get_chat(f"https://t.me/{chat.link}")).id
                )

            except Exception:
                logging.error("Can`t parse link")

        if message.chat.id in db_chats:
            for keyword in enabled_keywords:
                if keyword.word in message.text:
                    if message.link:
                        await client.send_message(
                            chat_id=keyword.owner_id,
                            text=TEXT["message_found_public"].format(
                                keyword=keyword.word,
                                link=message.link
                            )
                        )

                    else:
                        await client.send_message(
                            chat_id=keyword.owner_id,
                            text=TEXT["message_found_private"].format(
                                keyword=keyword.word,
                                chat=message.chat.title,
                                author=message.from_user.mention,
                                text=message.text
                            )
                        )

                    logging.info(f"Message: {message.link} parsed by keyword: {keyword.word}")  # noqa: E501
