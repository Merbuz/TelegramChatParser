from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram_patch.router import Router

if TYPE_CHECKING:
    from pyrogram.client import Client
    from pyrogram.types.messages_and_media import Message


message_router = Router()


@message_router.on_message()
async def message_handler(client: Client, message: Message):
    await message.reply(text="*Неизвестное сообщение.* Отправьте /start")
