from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any
)

from pyrogram_patch import patch
from pyrogram.client import Client

if TYPE_CHECKING:
    from pyrogram_patch.router import Router
    from pyrogram_patch.fsm.base_storage import BaseStorage


class Bot(Client):
    def include_middleware(self, middleware: Any) -> None:
        patch(self).include_middleware(middleware)

    def include_outer_middleware(self, middleware: Any) -> None:
        patch(self).include_outer_middleware(middleware)

    def set_storage(self, storage: BaseStorage) -> None:
        patch(self).set_storage(storage)

    def include_router(self, router: Router) -> None:
        patch(self).include_router(router)

    def include_routers(self, *routers: Router) -> None:
        for router in routers:
            self.include_router(router)
