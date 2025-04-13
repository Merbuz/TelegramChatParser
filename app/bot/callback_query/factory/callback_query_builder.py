from __future__ import annotations

import sys
import typing
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Type,
    TypeVar
)
from types import UnionType

from pyrogram import filters
from pyrogram.filters import Filter
from pyrogram.types import CallbackQuery
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined


T = TypeVar("T", bound="CallbackData")

MAX_CALLBACK_LENGTH = 64
_UNION_TYPES = {typing.Union}

if sys.version_info >= (3, 10):
    _UNION_TYPES.add(UnionType)


# Inspired from aiogram callback factory

class CallbackData(BaseModel):
    if TYPE_CHECKING:
        __separator__: ClassVar[str]
        __prefix__: ClassVar[str]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if "prefix" not in kwargs:
            raise ValueError("prefix required")

        cls.__separator__ = kwargs.pop("sep", ":")
        cls.__prefix__ = kwargs.pop("prefix")

        if cls.__separator__ in cls.__prefix__:
            raise ValueError(
                f"Separator symbol {cls.__separator__!r} can not be used "
                f"inside prefix {cls.__prefix__!r}"
            )

        super().__init_subclass__(**kwargs)

    def _encode_value(self, key: str, value: Any) -> str:
        if value is None:
            return ""

        if isinstance(value, bool):
            return str(int(value))

        if isinstance(value, (int, str, float)):
            return str(value)

        raise ValueError(
            f"Attribute {key}={value!r} of type {type(value).__name__!r}"
            f" can not be packed to callback data"
        )

    def pack(self) -> str:
        """Generate callback data string"""

        result = [self.__prefix__]

        for key, value in self.model_dump(mode="python").items():
            encoded = self._encode_value(key, value)

            if self.__separator__ in encoded:
                raise ValueError(
                    f"Separator symbol {self.__separator__!r} can not be used "
                    f"in value {key}={encoded!r}"
                )

            result.append(encoded)

        callback_data = self.__separator__.join(result)

        if len(callback_data.encode()) > MAX_CALLBACK_LENGTH:
            raise ValueError("Resulted callback data is too long!")

        return callback_data

    @classmethod
    def unpack(cls: Type[T], value: str | bytes) -> T:
        """Parse callback data string"""

        if isinstance(value, bytes):
            value = value.decode()

        elif isinstance(value, str):
            pass

        else:
            raise ValueError(f"Unknown value: {value}")

        prefix, *parts = value.split(cls.__separator__)
        names = cls.model_fields.keys()

        if len(parts) != len(names):
            raise TypeError(
                f"Callback data {cls.__name__!r} takes {len(names)} arguments "
                f"but {len(parts)} were given"
            )

        if prefix != cls.__prefix__:
            raise ValueError(f"Bad prefix ({prefix!r} != {cls.__prefix__!r})")

        payload = {}

        for k, v in zip(names, parts):
            if field := cls.model_fields.get(k):
                if v == "" and _check_field_is_nullable(field) and field.default != "":  # noqa: E501
                    v = field.default if field.default is not PydanticUndefined else None  # noqa: E501

            payload[k] = v

        return cls(**payload)

    @classmethod
    def filter(cls) -> Filter:
        async def func(_, __, query: CallbackQuery) -> bool:
            if isinstance(query, CallbackQuery) and query.data:
                if isinstance(query.data, bytes):
                    return query.data.decode().startswith(cls.__prefix__)

                elif isinstance(query.data, str):
                    return query.data.startswith(cls.__prefix__)

                else:
                    return False

            else:
                return False

        return filters.create(func)


def _check_field_is_nullable(field: FieldInfo) -> bool:
    if not field.is_required():
        return True

    return typing.get_origin(field.annotation) in _UNION_TYPES and type(None) in typing.get_args(  # noqa: E501
        field.annotation
    )
