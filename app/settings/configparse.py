import configparser
from typing import List


class Singleton:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Settings(Singleton):
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
        return self.parser.getboolean("Bot", "view_logs")
