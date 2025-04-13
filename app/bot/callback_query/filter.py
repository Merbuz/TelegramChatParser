from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram import filters

if TYPE_CHECKING:
    from pyrogram.filters import Filter
    from pyrogram.types import CallbackQuery


class CallbackFilter:
    @staticmethod
    def filter(data: str) -> Filter:
        async def func(flt, _, query: CallbackQuery):
            return flt.data == query.data

        return filters.create(func, data=data)
