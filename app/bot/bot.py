from __future__ import annotations

import os
from typing import (
    TYPE_CHECKING,
    Any
)

from dotenv import load_dotenv
from pyrogram_patch import patch
from pyrogram.client import Client
from typing_extensions import Self

if TYPE_CHECKING:
    from pyrogram_patch.router import Router
    from pyrogram_patch.fsm.base_storage import BaseStorage


class Bot(Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.patched = patch(self)

    @classmethod
    def from_env(cls, *args, **kwargs) -> Self:
        """Takes the data necessary for the bot from the .env file"""

        load_dotenv()

        API_ID = os.getenv("API_ID")
        API_HASH = os.getenv("API_HASH")
        BOT_TOKEN = os.getenv("BOT_TOKEN")

        if not API_ID or not API_ID.isdigit():
            raise Exception("API_ID in .env can't be empty or string")

        elif not API_HASH:
            raise Exception("API_HASH in .env can't be empty")

        elif not BOT_TOKEN:
            raise Exception("BOT_TOKEN in .env can't be empty")

        return cls(
            *args,
            **kwargs,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )

    def include_middleware(self, middleware: Any) -> None:
        self.patched.include_middleware(middleware)

    def include_outer_middleware(self, middleware: Any) -> None:
        self.patched.include_outer_middleware(middleware)

    def set_storage(self, storage: BaseStorage) -> None:
        self.patched.set_storage(storage)

    def include_router(self, router: Router) -> None:
        self.patched.include_router(router)

    def include_routers(self, *routers: Router) -> None:
        for router in routers:
            self.include_router(router)
