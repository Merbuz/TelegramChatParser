import logging
from pathlib import Path
from typing import List, Optional

from simple_singleton import ThreadSingletonArgs

from app.user.user import User
from app.user.handler import new_message_router
from app.db.db_requests import DB
from app.db.models import (
    Chats, Chat
)


class Parser(metaclass=ThreadSingletonArgs):
    def __init__(self) -> None:
        self.users = self.from_session_files_users
        self.parsing = False

        self._setup_routers()

    @property
    def from_session_files_users(self) -> List[User]:
        ext = ".session"
        path = Path("./sessions")
        sessions = [file for file in path.glob(f"*{ext}")]

        return [User.from_env(name=str(session).replace(ext, "")) for session in sessions]  # noqa: E501

    def _setup_routers(self) -> None:
        for user in self.users:
            user.include_router(new_message_router)

    def update(self) -> None:
        """Updates users in parser"""

        self.users = self.from_session_files_users

        self._setup_routers()

    async def join_chats(self) -> None:
        """Connects to chats by links in database"""

        chats: Optional[List[Chat]] = await DB.get_many(
            table_cls=Chats
        )

        if chats:
            for user in self.users:
                for chat in chats:
                    try:
                        await user.join_chat(f"https://t.me/{chat.link}")

                    except Exception as e:
                        logging.error(e)

    async def run(self) -> None:
        """Runs parser"""

        self.parsing = True

        for user in self.users:
            await user.user_start()

        await self.join_chats()

    async def stop(self) -> None:
        """Stops parser"""

        self.parsing = False

        for user in self.users:
            try:
                await user.stop()

                self.update()

            except Exception:
                pass
