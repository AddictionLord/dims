import sys
from typing import Any, Optional

from _pydevd_bundle.pydevd_extension_api import StrPresentationProvider


def _find_mod_attr(mod_name: str, attr_name: str) -> Optional[Any]:
    """Safely import a module and get an attribute.

    Args:
        mod_name: Fully qualified module name to import.
        attr_name: Attribute name to retrieve from the module.

    Returns:
        Optional[Any]: The requested attribute if found, None otherwise.

    """
    mod = sys.modules.get(mod_name)
    if mod is None:
        try:
            __import__(mod_name)
            mod = sys.modules[mod_name]
        except (ImportError, KeyError):
            return None

    return getattr(mod, attr_name, None)


class DimsShapeStr:
    """Display shape/size information for Sized objects in the debugger.

    Prepends shape or length information to variable string representations
    in the VSCode debug variables view. Objects with a .shape attribute
    (NumPy arrays, PyTorch tensors) show their shape. Other sized collections
    (list, dict, set, tuple) show their length. Strings are excluded to
    reduce noise.

    Attributes:
        None (stateless provider).

    """

    def can_provide(self, type_object: type, type_name: str) -> bool:
        """Check if this provider can format the given type.

        Args:
            type_object: The type to check.
            type_name: String name of the type (unused).

        Returns:
            bool: True if this provider handles the type, False otherwise.

        """
        if issubclass(type_object, str):
            return False

        sized_obj = _find_mod_attr("collections.abc", "Sized")
        if sized_obj is None:
            return False

        return issubclass(type_object, sized_obj)

    def get_str(self, val: Any) -> str:
        """Generate string representation with shape/size prefix.

        Args:
            val: The object to format.

        Returns:
            str: Formatted string with shape/size prefix, or fallback string.

        """
        try:
            if hasattr(val, "shape"):
                shape = val.shape
                return f"{{{list(shape)}}}, {val}"
            return f"{{{len(val)}}}, {val}"
        except Exception:
            return str(val)


if not sys.platform.startswith("java"):
    StrPresentationProvider.register(DimsShapeStr)
