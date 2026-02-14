"""
dims - Display shapes of arrays, tensors, and sized objects in the debugger.

This is a pydevd extension plugin that modifies how variables are displayed
in the VSCode debug variables view. It prepends shape/size information
to the string representation of objects that have a .shape attribute
or implement collections.abc.Sized.

Examples:
    ndarray:  {[2, 3]}, [[1 2 3]    →  shape is [2, 3]
    Tensor:   {[2, 3]}, tensor(...)  →  shape is [2, 3]
    list:     {3}, [1, 2, 3]        →  length is 3
    dict:     {2}, {1: 2, 3: 4}     →  length is 2
    set:      {3}, {1, 2, 3}        →  length is 3
    tuple:    {3}, (1, 2, 3)        →  length is 3
    str:      unchanged             →  strings are excluded (noisy)
"""

from typing import Any, Optional
from _pydevd_bundle.pydevd_extension_api import StrPresentationProvider


def _find_mod_attr(mod_name: str, attr_name: str) -> Optional[Any]:
    """Safely import a module and get an attribute, returning None on failure."""
    import sys
    try:
        mod = sys.modules.get(mod_name)
        if mod is None:
            __import__(mod_name)
            mod = sys.modules[mod_name]
        return getattr(mod, attr_name, None)
    except Exception:
        return None


class DimsShapeStr:
    """Displays the size/shape of a Sized object before displaying its value.

    For objects with a .shape attribute (numpy arrays, PyTorch tensors, etc.),
    shows the shape as a list: {[2, 3, 4]}, tensor(...)

    For other Sized objects (list, dict, set, tuple),
    shows the length: {3}, [1, 2, 3]

    Strings are excluded to avoid noise.
    """

    def can_provide(self, type_object: type, type_name: str) -> bool:
        # Exclude strings — showing length of every string is noise
        if issubclass(type_object, str):
            return False

        sized_obj = _find_mod_attr('collections.abc', 'Sized')
        return sized_obj is not None and issubclass(type_object, sized_obj)

    def get_str(self, val: Any) -> str:
        try:
            if hasattr(val, 'shape'):
                shape = val.shape
                # Handle both tuple shapes and torch.Size
                return '{%s}, %s' % (list(shape), val)
            return '{%s}, %s' % (len(val), val)
        except Exception:
            # Fallback: don't break the debugger if something goes wrong
            return str(val)


import sys

if not sys.platform.startswith("java"):
    StrPresentationProvider.register(DimsShapeStr)
