import math
from typing import (
    Optional,
    List
)
from pathlib import Path

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.db_requests import DB
from app.db.models import (
    Keywords, Keyword,
    Chats, Chat
)
from app.bot.markups.text import BUTTON
from app.bot.callback_query.callback_data import (
    KeywordData,
    KeywordParse,
    KeywordRemove,
    ChatData,
    ChatRemove,
    SessionData,
    SessionRemove
)
from app.parser.botnet import Parser


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
            ),
            InlineKeyboardButton(
                text=BUTTON["manage_parser"],
                callback_data="manage_parser"
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
                    text=BUTTON["need_to_parse"].format("yes" if keyword.enabled else "no"),  # noqa: E501
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
                text=BUTTON["add_link"],
                callback_data="add_link"
            ),
            InlineKeyboardButton(
                text=BUTTON["links_list"],
                callback_data="links_list"
            ),
            InlineKeyboardMenus._back("start")
        )

    @staticmethod
    async def links_list() -> InlineKeyboardMarkup:
        inline_menu: List[InlineKeyboardButton] = []
        links: Optional[List[Chat]] = await DB.get_many(
            table_cls=Chats
        )

        if links:
            for link in links:
                inline_menu.append(
                    InlineKeyboardButton(
                        text=link.link,
                        callback_data=ChatData(
                            link=link.link
                        ).pack()
                    )
                )

        return InlineKeyboardMenus._inline_keyboard_builder(
            *inline_menu,
            InlineKeyboardMenus._back("manage_links")
        )

    @staticmethod
    async def manage_link(link: str) -> InlineKeyboardMarkup:
        chat_link: Optional[Chat] = await DB.get(
            table_cls=Chats,
            sql_args=[
                "link"
            ],
            sql_values=[
                link
            ]
        )

        if chat_link:
            return InlineKeyboardMenus._inline_keyboard_builder(
                InlineKeyboardButton(
                    text=BUTTON["remove_link"],
                    callback_data=ChatRemove(
                        link=chat_link.link
                    ).pack()
                ),
                InlineKeyboardMenus._back(
                    data="links_list"
                )
            )

        else:
            return await InlineKeyboardMenus.back("links_list")

    @staticmethod
    async def manage_sessions() -> InlineKeyboardMarkup:
        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardButton(
                text=BUTTON["add_session"],
                callback_data="add_session"
            ),
            InlineKeyboardButton(
                text=BUTTON["sessions_list"],
                callback_data="sessions_list"
            ),
            InlineKeyboardMenus._back("start")
        )

    @staticmethod
    async def sessions_list() -> InlineKeyboardMarkup:
        inline_menu: List[InlineKeyboardButton] = []
        path = Path("./sessions")

        for file in path.glob("*.session"):
            inline_menu.append(
                InlineKeyboardButton(
                    text=file.name,
                    callback_data=SessionData(
                        name=file.name
                    ).pack()
                )
            )

        return InlineKeyboardMenus._inline_keyboard_builder(
            *inline_menu,
            InlineKeyboardMenus._back("manage_sessions")
        )

    @staticmethod
    async def manage_session(name: str) -> InlineKeyboardMarkup:
        session = Path(f"./sessions/{name}")

        if session.exists():
            return InlineKeyboardMenus._inline_keyboard_builder(
                InlineKeyboardButton(
                    text=BUTTON["remove_session"],
                    callback_data=SessionRemove(
                        name=name
                    ).pack()
                ),
                InlineKeyboardMenus._back(
                    data="sessions_list"
                )
            )

        else:
            return await InlineKeyboardMenus.back("sessions_list")

    @staticmethod
    async def manage_parser() -> InlineKeyboardMarkup:
        parser = Parser()

        return InlineKeyboardMenus._inline_keyboard_builder(
            InlineKeyboardButton(
                text=BUTTON["parsing"] + BUTTON["enabled" if parser.parsing else "disabled"],  # noqa: E501
                callback_data="parser_parsing"
            ),
            InlineKeyboardMenus._back("start")
        )
