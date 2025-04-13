from typing import List

from attrs import define


@define
class Keyword:
    word: str
    owner_id: int
    enabled: bool


@define
class Keywords:
    rows: List[Keyword]


@define
class Chat:
    link: str


@define
class Chats:
    rows: List[Chat]
