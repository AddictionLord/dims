import time
from typing import Any, Optional

import numpy as np
import pandas as pd
import pytest
from _pydevd_bundle import pydevd_xml
from _pydevd_bundle.pydevd_extension_api import StrPresentationProvider
from _pydevd_bundle.pydevd_extension_utils import extensions_of_type
from _pydevd_bundle.pydevd_safe_repr import SafeRepr


class BrokenLen:
    def __len__(self) -> int:
        raise RuntimeError


def display(val: Any, context: Optional[str] = None) -> str:
    return pydevd_xml.get_variable_details(val, to_string=SafeRepr(), context=context)[-1]


def test_plugin_is_discovered() -> None:
    """The plugin is loaded from the extra PYTHONPATH entry."""
    names = [type(provider).__name__ for provider in extensions_of_type(StrPresentationProvider)]
    assert "DimsShapeStr" in names


@pytest.mark.parametrize(
    ("val", "prefix"),
    [
        (np.zeros((2, 3)), "{[2, 3]}, array("),
        (np.array(1.0), "{[]}, array("),
        ([1, 2, 3], "{3}, [1, 2, 3]"),
        ((1, 2), "{2}, (1, 2)"),
        ({1: 2}, "{1}, {1: 2}"),
        ({1, 2, 3}, "{3}, {1, 2, 3}"),
        (range(5), "{5}, range(0, 5)"),
        (pd.DataFrame({"a": [1, 2]}), "{[2, 1]}, "),
        (pd.Series([1, 2, 3]), "{[3]}, "),
    ],
)
def test_prefix(val: Any, prefix: str) -> None:
    """Sized values get their shape or length prepended."""
    assert display(val).startswith(prefix)


@pytest.mark.parametrize("val", ["hello", b"hello", bytearray(b"hello")])
def test_strings_unchanged(val: Any) -> None:
    """Strings and bytes are left to pydevd."""
    assert not display(val).startswith("{")


def test_clipboard_has_no_prefix() -> None:
    """Copy Value yields the plain repr."""
    assert display([1, 2, 3], context="clipboard") == "[1, 2, 3]"


def test_broken_len_falls_back_to_repr() -> None:
    """A raising __len__ does not break the variable view."""
    assert display(BrokenLen()).startswith("<")


def test_large_list_is_bounded() -> None:
    """A huge list is rendered through SafeRepr, not str()."""
    big = list(range(5_000_000))
    start = time.perf_counter()
    value = display(big)
    elapsed = time.perf_counter() - start
    assert value.startswith("{5000000}, [0, 1, 2")
    assert len(value) < 10_000
    assert elapsed < 0.1


def test_torch_tensor() -> None:
    """Tensors show torch.Size as a list."""
    torch = pytest.importorskip("torch")
    assert display(torch.zeros(2, 3)).startswith("{[2, 3]}, tensor(")
