from dataclasses import (
    dataclass,
)
from fa_purity import (
    _iter_factory,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.pure_iter._inner import (
    InnerPureIter,
)
from fa_purity.pure_iter.core import (
    PureIter,
)
from itertools import (
    count,
)
from typing import (
    Callable,
    Iterable,
    List,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
_I = TypeVar("_I")
_R = TypeVar("_R")


def unsafe_from_cmd(cmd: Cmd[Iterable[_T]]) -> PureIter[_T]:
    # [WARNING] unsafe constructor
    # - Type-check cannot ensure its proper use
    # - Do not use until is strictly necessary
    # - Do unit test over the function defined by this, i.e. assert reproducibility
    #
    # Cmd argument MUST produce semanticly equivalent iterables. This is:
    # possibly different objects that means the same thing
    #
    # - if Iterable is IMMUTABLE (e.g. tuple) then requirement is fulfilled
    # - if Iterable is MUTABLE then the Cmd must call the obj constructor (that is not pure)
    # with the same arguments for ensuring equivalence.
    #
    # Non compliant code:
    #   y = map(lambda i: i + 1, range(0, 10))
    #   x = unsafe_from_cmd(
    #       Cmd.from_cmd(lambda: y)
    #   )
    #   # y is a map obj instance; cmd lambda is pinned with a single ref
    #   # since map is MUTABLE the ref should change at every call
    #
    # Compliant code:
    #   x = unsafe_from_cmd(
    #       Cmd.from_cmd(
    #           lambda: map(lambda i: i + 1, range(0, 10))
    #       )
    #   )
    #   # cmd lambda produces a new ref in each call
    #   # but all of them are equivalent (created with the same args)
    return PureIter(InnerPureIter(cmd))


def from_flist(items: FrozenList[_T]) -> PureIter[_T]:
    return unsafe_from_cmd(Cmd.from_cmd(lambda: items))


@dataclass(frozen=True)
class PureIterFactory:
    "`PureIter` safe constructors"

    @staticmethod
    def from_list(items: Union[List[_T], FrozenList[_T]]) -> PureIter[_T]:
        _items = tuple(items) if isinstance(items, list) else items
        return from_flist(_items)

    @staticmethod
    def from_range(range_obj: range) -> PureIter[int]:
        return unsafe_from_cmd(Cmd.from_cmd(lambda: range_obj))

    @staticmethod
    def infinite_gen(function: Callable[[_T], _T], init: _T) -> PureIter[_T]:
        return unsafe_from_cmd(
            Cmd.from_cmd(lambda: _iter_factory.infinite_gen(function, init))
        )

    @staticmethod
    def infinite_range(start: int, step: int) -> PureIter[int]:
        return unsafe_from_cmd(Cmd.from_cmd(lambda: count(start, step)))

    @staticmethod
    def pure_map(
        function: Callable[[_I], _R], items: Union[List[_I], FrozenList[_I]]
    ) -> PureIter[_R]:
        return from_list(items).map(function)


from_list = PureIterFactory.from_list
from_range = PureIterFactory.from_range
infinite_gen = PureIterFactory.infinite_gen
infinite_range = PureIterFactory.infinite_range
pure_map = PureIterFactory.pure_map
