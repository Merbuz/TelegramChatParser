from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram_patch.router import Router

from app.bot.callback_query.filter import CallbackFilter
from app.bot.callback_query.callback_data import ExampleData

if TYPE_CHECKING:
    from pyrogram.client import Client
    from pyrogram.types import CallbackQuery


callback_router = Router()


@callback_router.on_callback_query(CallbackFilter.filter("manage_keywords"))


@callback_router.on_callback_query(ExampleData.filter())
async def start(client: Client, callback_query: CallbackQuery):
    callback_data = ExampleData.unpack(callback_query.data)

    await callback_query.answer(text=f"**📄 Парсер {callback_data.data}**")
