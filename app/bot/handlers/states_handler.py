from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.filters import command
from pyrogram_patch.router import Router
from pyrogram_patch.fsm.filter import StateFilter

if TYPE_CHECKING:
    from pyrogram.client import Client
    from pyrogram.types.messages_and_media import Message


command_router = Router()


@command_router.on_message(StateFilter())
async def example(client: Client, message: Message):
    await message.reply(text="**📄 Меню управления парсером**")
