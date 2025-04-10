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
class PublicChat:
    id: int
    status: str


@define
class PublicChats:
    rows: List[PublicChat]


@define
class PrivateChat:
    id: int
    status: str


@define
class PrivateChats:
    rows: List[PrivateChat]
