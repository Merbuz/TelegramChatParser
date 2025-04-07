from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.filters import command

from app.bot.router import Router

if TYPE_CHECKING:
    from pyrogram.client import Client
    from pyrogram.types.messages_and_media import Message


command_router = Router("Commands")


@command_router.on_message(command("start"))
async def start(client: Client, message: Message):
    await message.reply(text="**📄 Меню управления парсером**")
