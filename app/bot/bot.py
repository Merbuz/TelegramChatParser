from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pyrogram.client import Client

if TYPE_CHECKING:
    from app.bot.router import Router


class Bot(Client):
    def include_router(self, router: Router) -> None:
        """Connects the handlers of the specified router"""

        logging.info(f"Including Router - {router.name}")

        for handler in router.handlers:
            self.add_handler(handler)

    def include_routers(self, *routers: Router) -> None:
        """Connects the handlers of the specified routers"""

        for router in routers:
            self.include_router(router)
