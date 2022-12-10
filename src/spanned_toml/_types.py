# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Jérome Eertmans, Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.
from collections.abc import Iterable, Iterator
from typing import Any, Callable, Generic, Tuple, TypeVar, Union

# Type annotations
ParseFloat = Callable[[str], Any]
Key = Tuple["Spanned[str]", ...]
Pos = int

T = TypeVar("T")


class Spanned(Generic[T]):
    """
    Generic container of any object, with span information.

    Nested objects must also have a span (which can optionally be empty).
    """
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

    def __getitem__(self, key: Union["Spanned[str]", int, slice]) -> "Spanned[Any]":
        if isinstance(self.__inner, dict):
            return self.__inner[key]
        elif isinstance(self.__inner, list):
            return self.__inner[key]
        else:
            raise KeyError(
                f"Unsupported key type {type(key)} for object type {type(self.__inner)}"
            )

    def __setitem__(self, key: "Spanned[str]", value: "Spanned[Any]") -> None:
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
        """
        Return the inner object, i.e., the object without its span information.
        """
        return self.__inner

    def span(self) -> slice:
        """
        Return the span of the current object as a slice.
        """
        return slice(self.__start, self.__end)

    def with_span(self, start: int, end: int) -> "Spanned[T]":
        """
        Update the span of the current object.
        """
        self.__start = start
        self.__end = end
        return self

    def unspan(self) -> Any:
        """
        Recursively unspan a spanned object.
        """
        if isinstance(self.__inner, dict):
            return {key.unspan(): value.unspan() for key, value in self.__inner.items()}
        elif isinstance(self.__inner, list):
            return [v.unspan() for v in self.__inner]
        elif isinstance(self.__inner, Spanned):
            return self.__inner.unspan()
        else:
            return self.__inner
