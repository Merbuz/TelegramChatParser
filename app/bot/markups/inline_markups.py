import math
from typing import List

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboardMenus:
    @staticmethod
    def _inline_keyboard_builder(
        *buttons: InlineKeyboardButton,
        row: int = 1
    ) -> InlineKeyboardMarkup:
        """Builds InlineKeyboardMarkup from buttons"""

        markup_buttons: List[tuple[InlineKeyboardButton, ...]] = []
        rows_count = math.ceil(len(buttons) / row)

        for i in range(1, rows_count + 1):
            markup_buttons.append(buttons[(i - 1) * row:(i - 1) + row])

        return InlineKeyboardMarkup(markup_buttons)  # type: ignore

    @staticmethod
    def start() -> InlineKeyboardMarkup:
        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardButton(
                text="⚙️ Управление ключевыми словами",
                callback_data="manage_keywords"
            ),
            InlineKeyboardButton(
                text="👥 Управление сессиями парсера",
                callback_data="manage_sessions"
            )
        )
