from __future__ import annotations

import os
import logging
from typing import (
    TYPE_CHECKING,
    Optional,
    Callable,
    TypeVar,
    Any
)

from dotenv import load_dotenv
from pyrogram_patch import patch
from pyrogram.raw import functions
from pyrogram.client import Client
from typing_extensions import Self

if TYPE_CHECKING:
    from pyrogram_patch.router import Router
    from pyrogram_patch.fsm.base_storage import BaseStorage


T = TypeVar("T", bound=Callable)


class User(Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(system_version="4.16.30-vxCUSTOM", *args, **kwargs)

        self.patched = patch(self)

    @classmethod
    def from_env(cls, *args, **kwargs) -> Self:
        """Takes the data necessary for the user from the .env file"""

        load_dotenv()

        API_ID = os.getenv("API_ID")
        API_HASH = os.getenv("API_HASH")

        if not API_ID or not API_ID.isdigit():
            raise Exception("API_ID in .env can't be empty or string")

        elif not API_HASH:
            raise Exception("API_HASH in .env can't be empty")

        return cls(
            *args,
            **kwargs,
            api_id=API_ID,
            api_hash=API_HASH
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

    async def is_valid(self) -> Optional[bool]:
        try:
            logging.info("Connecting...")

            await self.connect()

            logging.info("Getting me...")

            await self.get_me()

        except Exception:
            try:
                logging.info("Disconnecting..")

                await self.disconnect()

            except Exception:
                logging.warning("Already disconnected")

                await self.storage.close()

                return False

        else:
            logging.info("Disconnecting..")

            await self.disconnect()

            return True

    async def user_start(self) -> Self:
        """Runs user instead of \"start\" function"""

        await self.connect()

        try:
            if self.takeout and not await self.storage.is_bot():
                self.takeout_id = (await self.invoke(functions.account.InitTakeoutSession())).id  # noqa: E501  # type: ignore
                logging.info("Takeout session %s initiated", self.takeout_id)

            await self.invoke(functions.updates.GetState())  # type: ignore

        except (Exception, KeyboardInterrupt):
            await self.disconnect()
            raise

        else:
            self.me = await self.get_me()
            await self.initialize()

            return self
