from __future__ import annotations

import contextlib
from typing import AsyncIterable, AsyncIterator, TypeVar

T = TypeVar("T")


@contextlib.asynccontextmanager
async def async_null_context(obj: T) -> AsyncIterator[T]:
    yield obj


async def async_enumerate(iterable: AsyncIterator[T] | AsyncIterable[T]):
    i = 0
    async for x in iterable:
        yield i, x
        i += 1
