from deprecated import (
    deprecated,
)
from fa_purity.frozen import (
    FrozenDict,
    unfreeze,
)
from fa_purity.json.factory import (
    JsonObj,
)
from fa_purity.json.value import (
    transform as jval_transform,
)
from fa_purity.json.value.core import (
    JsonValue,
)
from simplejson import (
    dumps as _dumps,
    JSONEncoder,
)
from typing import (
    Any,
    Dict,
    TypeVar,
)


@deprecated("Replaced. Use `fa_purity.json_2.Unfolder` instead")  # type: ignore[misc]
def to_raw(json_obj: JsonObj) -> Dict[str, Any]:
    return {key: jval_transform.to_raw(val) for key, val in json_obj.items()}  # type: ignore[misc]


_T = TypeVar("_T")


class _JsonEncoder(JSONEncoder):
    def default(self: JSONEncoder, o: _T) -> Any:  # type: ignore[misc]
        if isinstance(o, FrozenDict):
            return unfreeze(o)  # type: ignore[misc]
        if isinstance(o, JsonValue):
            return o.unfold()
        return JSONEncoder.default(self, o)  # type: ignore[misc]


@deprecated("Replaced. Use `fa_purity.json_2.Unfolder` instead")  # type: ignore[misc]
def dumps(obj: JsonObj) -> str:
    return _dumps(obj, cls=_JsonEncoder)  # type: ignore[misc]
