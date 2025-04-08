from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.filters import command
from pyrogram_patch.router import Router

from app.bot.markups.inline_markups import InlineKeyboardMenus

if TYPE_CHECKING:
    from pyrogram.client import Client
    from pyrogram.types.messages_and_media import Message


command_router = Router()


@command_router.on_message(command("start"))
async def start(client: Client, message: Message):
    await message.reply(
        text="**📄 Добро пожаловать в меню управления парсером!\n\n"
        "Выберите действие**",
        reply_markup=InlineKeyboardMenus.start()
    )
