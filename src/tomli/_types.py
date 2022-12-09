# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.
from collections.abc import Iterable, Iterator
from typing import Any, Callable, Generic, Tuple, TypeVar

# Type annotations
ParseFloat = Callable[[str], Any]
Key = Tuple["Spanned[str]", ...]
Pos = int

T = TypeVar("T")


class Spanned(Generic[T]):
    def __init__(self, inner: T, start: int = 0, end: int = 0) -> None:
        self.__inner = inner
        self.__start = start
        self.__end = end

    def __iter__(self) -> Iterator:
        if isinstance(self.__inner, Iterable):
            return self.__inner.__iter__()
        else:
            raise ValueError(f"__iter__ not supported for {self.__inner}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Spanned):
            return self.__inner == other.__inner
        else:
            return self.__inner == other

    def __getitem__(self, key: "Spanned[str]") -> "Spanned[Any]":
        if isinstance(self.__inner, dict):
            return self.__inner[key]
        else:
            raise KeyError(
                f"Unsupported key type {type(key)} for object type {type(self.__inner)}"
            )

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(self.__inner, dict):
            self.__inner.__setitem__(key, value)
        else:
            raise ValueError(f"Cannot set value of {self.__inner}")

    def __getattr__(self, key: str) -> Any:
        return getattr(self.__inner, key)

    def __hash__(self) -> int:
        return hash(self.__inner)

    def __str__(self) -> str:
        return str(self.__inner)

    def __repr__(self) -> str:
        return "Spanned(%s, %d:%d)" % (repr(self.__inner), self.__start, self.__end)

    def inner(self) -> T:
        return self.__inner

    def span(self) -> slice:
        return slice(self.__start, self.__end)

    def offset_by(self, offset: int) -> "Spanned":
        self.__start += offset
        self.__end += offset
        return self
