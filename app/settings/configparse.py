import configparser
from typing import (
    List,
    Any
)


class Singleton:
    def __init__(self, cls: Any):
        self.wrapped = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self.wrapped(*args, **kwargs)

        return self._instance


def singleton(cls):
    return Singleton(cls)


@singleton
class Settings:
    def __init__(self):
        self.parser = configparser.ConfigParser()

        self._read()

    def _read(self) -> List[str]:
        return self.parser.read("settings.ini", encoding="utf-8")

    @property
    def white_list(self) -> List[int]:
        return list(map(int, self.parser.get("Bot", "white_list").split(",")))

    @property
    def view_logs(self) -> bool:
        return self.parser.getboolean("Bot", "view.logs")
