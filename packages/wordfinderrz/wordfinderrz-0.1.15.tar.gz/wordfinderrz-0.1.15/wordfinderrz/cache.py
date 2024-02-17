from collections import OrderedDict
from collections.abc import Callable, Hashable
from functools import update_wrapper
from typing import Generic, ParamSpec, TypeVar, cast, overload

P = ParamSpec("P")
T = TypeVar("T")


class _SENTINEL: ...


class Cache(Generic[P, T]):
    """LRU cache for functions with hashable parameters."""

    def __init__(
        self,
        func: Callable[P, T],
        /,
        maxsize: int | None = 128,
        typed: bool = False,
    ) -> None:
        self.func: Callable[P, T] = func
        self.cache: OrderedDict[Hashable, T] = OrderedDict()
        self.hits = self.misses = 0
        self.maxsize = maxsize
        self.typed = typed
        update_wrapper(self, func)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        key = Cache._make_key(args, kwargs, self.typed)
        cached_result = self._cache_get(key)
        if cached_result is _SENTINEL:
            self.misses += 1
            result = self.func(*args, **kwargs)
            self.cache[key] = result
            if self.maxsize is not None and len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)
            return result
        else:
            self.hits += 1
            return cast(T, cached_result)

    def _cache_get(self, key: Hashable) -> T | type[_SENTINEL]:
        return self.cache.get(key, _SENTINEL)

    @staticmethod
    def _make_key(
        args: tuple[Hashable, ...], kwargs: dict[str, Hashable], typed: bool
    ) -> Hashable:
        result = *args, _SENTINEL, *kwargs.items()
        if typed:
            result += (
                _SENTINEL,
                *(type(arg) for arg in args),
                _SENTINEL,
                *((k, type(v)) for k, v in kwargs.items()),
            )
        return result


@overload
def lru_cache(
    func: Callable[P, T],
    /,
    maxsize: int | None = 128,
    typed: bool = False,
) -> Cache[P, T]: ...


@overload
def lru_cache(
    func: None = None,
    /,
    maxsize: int | None = 128,
    typed: bool = False,
) -> Callable[[Callable[P, T]], Cache[P, T]]: ...


def lru_cache(
    func: Callable[P, T] | None = None,
    /,
    maxsize: int | None = 128,
    typed: bool = False,
) -> Cache[P, T] | Callable[[Callable[P, T]], Cache[P, T]]:
    """LRU cache for functions with hashable parameters."""
    if func is None:
        return lambda fn: Cache(fn, maxsize=maxsize, typed=typed)
    return Cache(func, maxsize, typed)


def cache(func: Callable[P, T]) -> Cache[P, T]:
    """Cache for functions with hashable parameters."""
    return Cache(func, maxsize=None, typed=False)
