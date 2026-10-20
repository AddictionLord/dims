"""dims: prepend the shape or length of sized objects to their debugger value.

Loaded by pydevd from the `pydevd_plugins.extensions` namespace package, which
the dims VS Code extension puts on PYTHONPATH of the debuggee.

Examples:
    ndarray:    {[2, 3]}, array([[0., 0., 0.], [0., 0., 0.]])
    Tensor:     {[2, 3]}, tensor([[0., 0., 0.], [0., 0., 0.]])
    DataFrame:  {[2, 1]},    a ...
    list:       {3}, [1, 2, 3]
    str, bytes: unchanged

Set Value in the Variables and Watch views starts from the displayed text, so
the prefix is stripped from setVariable/setExpression values before pydevd
evaluates them.
"""

import collections.abc
import re
import sys
from typing import Any, Callable, List, Optional, Tuple

from _pydev_bundle import pydev_log
from _pydevd_bundle.pydevd_extension_api import StrPresentationProvider
from _pydevd_bundle.pydevd_safe_repr import SafeRepr

try:
    from pydevd_plugins.extensions.types import pydevd_plugin_pandas_types
except Exception:
    pydevd_plugin_pandas_types = None

try:
    from _pydevd_bundle.pydevd_process_net_command_json import PyDevJsonCommandProcessor
except Exception:
    PyDevJsonCommandProcessor = None

EXCLUDED_TYPES: Tuple[type, ...] = (str, bytes, bytearray)
PLAIN_CONTEXTS: Tuple[str, ...] = ("clipboard",)
PANDAS_PROVIDER_NAMES: List[str] = [
    "PandasDataFrameTypeResolveProvider",
    "PandasSeriesTypeResolveProvider",
]
SET_VALUE_HANDLERS: List[str] = [
    "on_setvariable_request",
    "on_setexpression_request",
]
DIMS_PREFIX = re.compile(r"\{(?:\[[\d, ]*\]|\d+)\}, ")

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


def strip_dims(text: str) -> str:
    match = DIMS_PREFIX.match(text)
    return text[match.end() :] if match else text


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


def patch_set_value_handlers() -> None:
    if PyDevJsonCommandProcessor is None:
        return

    for name in SET_VALUE_HANDLERS:
        handler = getattr(PyDevJsonCommandProcessor, name, None)
        if handler is None or getattr(handler, "_dims_patched", False):
            continue
        setattr(PyDevJsonCommandProcessor, name, wrap_set_value(handler))


def wrap_set_value(handler: Callable[[Any, Any, Any], Any]) -> Callable[[Any, Any, Any], Any]:
    def set_value_without_dims(self: Any, py_db: Any, request: Any) -> Any:
        arguments = request.arguments
        value = getattr(arguments, "value", None)
        if isinstance(value, str):
            arguments.value = strip_dims(value)
        return handler(self, py_db, request)

    set_value_without_dims._dims_patched = True
    return set_value_without_dims


if not sys.platform.startswith("java"):
    StrPresentationProvider.register(DimsShapeStr)
    try:
        patch_pandas_providers()
    except Exception:
        pydev_log.exception("dims: unable to patch pandas providers")
    try:
        patch_set_value_handlers()
    except Exception:
        pydev_log.exception("dims: unable to patch set value handlers")
