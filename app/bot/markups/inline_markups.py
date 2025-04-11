import math
from typing import (
    Optional,
    List
)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.db_requests import DB
from app.db.models import (
    Keywords, Keyword,
    PublicChats, PublicChat,
    PrivateChats, PrivateChat
)
from app.bot.markups.text import BUTTON
from app.bot.callback_query.callback_data import (
    KeywordData,
    KeywordParse,
    KeywordRemove
)


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
    def _back(data: str) -> InlineKeyboardButton:
        """This is just a back button. Don`t use it"""

        return InlineKeyboardButton(text=BUTTON["back"], callback_data=data)

    @staticmethod
    async def back(data: str) -> InlineKeyboardMarkup:
        """Back inline menu"""

        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardMenus._back(data=data)
        )

    @staticmethod
    async def start() -> InlineKeyboardMarkup:
        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardButton(
                text=BUTTON["manage_keywords"],
                callback_data="manage_keywords"
            ),
            InlineKeyboardButton(
                text=BUTTON["manage_links"],
                callback_data="manage_links"
            ),
            InlineKeyboardButton(
                text=BUTTON["manage_sessions"],
                callback_data="manage_sessions"
            )
        )

    @staticmethod
    async def manage_keywords() -> InlineKeyboardMarkup:
        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardButton(
                text=BUTTON["add_keyword"],
                callback_data="add_keyword"
            ),
            InlineKeyboardButton(
                text=BUTTON["keywords_list"],
                callback_data="keywords_list"
            ),
            InlineKeyboardMenus._back("start")
        )

    @staticmethod
    async def keywords_list(owner_id: int) -> InlineKeyboardMarkup:
        inline_menu: List[InlineKeyboardButton] = []
        keywords: Optional[List[Keyword]] = await DB.get_many(
            table_cls=Keywords,
            sql_args=[
                "owner_id"
            ],
            sql_values=[
                owner_id
            ]
        )

        if keywords:
            for keyword in keywords:
                inline_menu.append(
                    InlineKeyboardButton(
                        text=keyword.word,
                        callback_data=KeywordData(
                            word=keyword.word
                        ).pack()
                    )
                )

        return InlineKeyboardMenus._inline_keyboard_builder(
            *inline_menu,
            InlineKeyboardMenus._back("manage_keywords")
        )

    @staticmethod
    async def manage_keyword(word: str) -> InlineKeyboardMarkup:
        keyword: Optional[Keyword] = await DB.get(
            table_cls=Keywords,
            sql_args=[
                "word"
            ],
            sql_values=[
                word
            ]
        )

        if keyword:
            return InlineKeyboardMenus._inline_keyboard_builder(
                InlineKeyboardButton(
                    text=BUTTON["need_to_parse"] + BUTTON["yes" if keyword.enabled else "no"],  # noqa: E501
                    callback_data=KeywordParse(
                        word=word
                    ).pack()
                ),
                InlineKeyboardButton(
                    text=BUTTON["remove_keyword"],
                    callback_data=KeywordRemove(
                        word=word
                    ).pack()
                ),
                InlineKeyboardMenus._back("keywords_list")
            )

        else:
            return await InlineKeyboardMenus.back("keywords_list")

    @staticmethod
    async def manage_links() -> InlineKeyboardMarkup:
        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardButton(
                text=BUTTON["public_links"],
                callback_data="public_links"
            ),
            InlineKeyboardButton(
                text=BUTTON["private_links"],
                callback_data="private_links"
            ),
            InlineKeyboardMenus._back(
                data="start"
            )
        )

    @staticmethod
    async def manage_public_links() -> InlineKeyboardMarkup:
        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardButton(
                text=BUTTON["add_link"],
                callback_data="add_public_link"
            ),
            InlineKeyboardButton(
                text=BUTTON["links_list"],
                callback_data="public_links_list"
            ),
            InlineKeyboardMenus._back("manage_links")
        )

    @staticmethod
    async def manage_private_links() -> InlineKeyboardMarkup:
        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardButton(
                text=BUTTON["add_link"],
                callback_data="add_private_link"
            ),
            InlineKeyboardButton(
                text=BUTTON["links_list"],
                callback_data="private_links_list"
            ),
            InlineKeyboardMenus._back("manage_links")
        )

    @staticmethod
    async def public_links_list() -> InlineKeyboardMarkup:
        inline_menu: List[InlineKeyboardButton] = []
        links: Optional[List[PublicChat]] = await DB.get_many(
            table_cls=PublicChats
        )

        if links:
            for link in links:
                inline_menu.append(
                    InlineKeyboardButton(
                        text=link.link,
                        callback_data=str(link.id)
                    )
                )

        return InlineKeyboardMenus._inline_keyboard_builder(
            *inline_menu,
            InlineKeyboardMenus._back("public_links")
        )

    @staticmethod
    async def private_links_list() -> InlineKeyboardMarkup:
        inline_menu: List[InlineKeyboardButton] = []
        links: Optional[List[PrivateChat]] = await DB.get_many(
            table_cls=PrivateChats
        )

        if links:
            for link in links:
                inline_menu.append(
                    InlineKeyboardButton(
                        text=link.link,
                        callback_data=str(link.id)
                    )
                )

        return InlineKeyboardMenus._inline_keyboard_builder(
            *inline_menu,
            InlineKeyboardMenus._back("private_links")
        )
