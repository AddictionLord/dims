"""dims: prepend the shape or length of sized objects to their debugger value.

Loaded by pydevd from the `pydevd_plugins.extensions` namespace package, which
the dims VS Code extension puts on PYTHONPATH of the debuggee.

Examples:
    ndarray:    {[2, 3]}, array([[0., 0., 0.], [0., 0., 0.]])
    Tensor:     {[2, 3]}, tensor([[0., 0., 0.], [0., 0., 0.]])
    DataFrame:  {[2, 1]},    a ...
    list:       {3}, [1, 2, 3]
    str, bytes: unchanged
"""

import collections.abc
import sys
from typing import Any, Callable, List, Optional, Tuple

from _pydev_bundle import pydev_log
from _pydevd_bundle.pydevd_extension_api import StrPresentationProvider
from _pydevd_bundle.pydevd_safe_repr import SafeRepr

try:
    from pydevd_plugins.extensions.types import pydevd_plugin_pandas_types
except Exception:
    pydevd_plugin_pandas_types = None

EXCLUDED_TYPES: Tuple[type, ...] = (str, bytes, bytearray)
PLAIN_CONTEXTS: Tuple[str, ...] = ("clipboard",)
PANDAS_PROVIDER_NAMES: List[str] = [
    "PandasDataFrameTypeResolveProvider",
    "PandasSeriesTypeResolveProvider",
]

_safe_repr = SafeRepr()


def format_dims(val: Any) -> Optional[str]:
    try:
        shape = getattr(val, "shape", None)
        if shape is not None:
            return "{%s}" % (list(shape),)
        return "{%d}" % (len(val),)
    except Exception:
        return None


def with_dims(val: Any, text: str) -> str:
    dims = format_dims(val)
    if dims is None:
        return text
    return "%s, %s" % (dims, text)


class DimsShapeStr:
    def can_provide(self, type_object: type, type_name: str) -> bool:
        if issubclass(type_object, EXCLUDED_TYPES):
            return False
        return issubclass(type_object, collections.abc.Sized)

    def get_str_in_context(self, val: Any, context: str) -> str:
        if context in PLAIN_CONTEXTS:
            return _safe_repr(val)
        return self.get_str(val)

    def get_str(self, val: Any) -> str:
        return with_dims(val, _safe_repr(val))


def patch_pandas_providers() -> None:
    if pydevd_plugin_pandas_types is None:
        return

    for name in PANDAS_PROVIDER_NAMES:
        provider = getattr(pydevd_plugin_pandas_types, name, None)
        if provider is None or getattr(provider.get_str, "_dims_patched", False):
            continue
        provider.get_str = wrap_get_str(provider.get_str)


def wrap_get_str(get_str: Callable[[Any, Any], str]) -> Callable[[Any, Any], str]:
    def get_str_with_dims(self: Any, val: Any) -> str:
        return with_dims(val, get_str(self, val))

    get_str_with_dims._dims_patched = True
    return get_str_with_dims


if not sys.platform.startswith("java"):
    StrPresentationProvider.register(DimsShapeStr)
    try:
        patch_pandas_providers()
    except Exception:
        pydev_log.exception("dims: unable to patch pandas providers")
