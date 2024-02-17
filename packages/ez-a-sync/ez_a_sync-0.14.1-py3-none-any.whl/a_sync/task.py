
import asyncio
import logging

from a_sync._typing import *
from a_sync import exceptions
from a_sync.utils.iterators import as_yielded
from a_sync.utils.as_completed import as_completed


logger = logging.getLogger(__name__)

def create_task(coro: Awaitable[T], *, name: Optional[str] = None, skip_gc_until_done: bool = False) -> "asyncio.Task[T]":
    """A wrapper over `asyncio.create_task` which will work with any `Awaitable` object, not just `Coroutine` objects"""
    if not asyncio.iscoroutine(coro):
        coro = __await(coro)
    task = asyncio.create_task(coro, name=name)
    if skip_gc_until_done:
        __persist(task)
    return task

class TaskMapping(DefaultDict[K, "asyncio.Task[V]"]):
    def __init__(self, coro_fn: Callable[Concatenate[K, P], Awaitable[V]] = None, *, name: str = '', **coro_fn_kwargs: P.kwargs) -> None:
        self._coro_fn = coro_fn
        self._coro_fn_kwargs = coro_fn_kwargs
        self._name = name
    def __setitem__(self, item: Any, value: Any) -> None:
        raise NotImplementedError("You cannot manually set items in a TaskMapping")
    def __getitem__(self, item: K) -> "asyncio.Task[V]":
        try:
            return super().__getitem__(item)
        except KeyError:
            task = create_task(
                coro=self._coro_fn(item, **self._coro_fn_kwargs),
                name=f"{self._name}[{item}]" if self._name else f"{item}",
            )
            super().__setitem__(item, task)
            return task
    async def map(self, *iterables: AnyIterable[K], pop: bool = True, yields: Literal['keys', 'both'] = 'both') -> AsyncIterator[Tuple[K, V]]:
        if self:
            raise exceptions.MappingNotEmptyError
        async for key in as_yielded(*[_yield_keys(iterable) for iterable in iterables]):  # type: ignore [attr-defined]
            self[key]  # ensure task is running
            async for key, value in self.yield_completed(pop=pop):
                yield _yield(key, value, yields)
        async for key, value in as_completed(self, aiter=True):
            yield _yield(key, value, yields)
    async def yield_completed(self, pop: bool = True) -> AsyncIterator[Tuple[K, V]]:
        for k, task in dict(self).items():
            if task.done():
                if pop:
                    task = self.pop(k)
                yield k, await task


__persisted_tasks: Set["asyncio.Task[Any]"] = set()

async def __await(awaitable: Awaitable[T]) -> T:
    return await awaitable

def __persist(task: "asyncio.Task[Any]") -> None:
    __persisted_tasks.add(task)
    __prune_persisted_tasks()

def __prune_persisted_tasks():
    for task in tuple(__persisted_tasks):
        if task.done():
            if e := task.exception():
                logger.exception(e)
                raise e
            __persisted_tasks.discard(task)

@overload
def _yield(key: K, value: V, yields: Literal['keys']) -> K:...
@overload
def _yield(key: K, value: V, yields: Literal['both']) -> Tuple[K, V]:...
def _yield(key: K, value: V, yields: Literal['keys', 'both']) -> Union[K, Tuple[K, V]]:
    if yields == 'both':
        return key, value
    elif yields == 'keys':
        return key
    else:
        raise ValueError(f"`yields` must be 'keys' or 'both'. You passed {yields}")

async def _yield_keys(iterable: AnyIterable[K]) -> AsyncIterator[K]:
    if isinstance(iterable, AsyncIterable):
        async for key in iterable:
            yield key
    elif isinstance(iterable, Iterable):
        for key in iterable:
            yield key
    else:
        raise TypeError(iterable)
