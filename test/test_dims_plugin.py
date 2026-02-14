import os
import sys
from unittest.mock import Mock

import numpy as np
import pytest

try:
    import debugpy

    debugpy_path = os.path.join(
        os.path.dirname(debugpy.__file__), "_vendored", "pydevd"
    )
    sys.path.insert(0, debugpy_path)
except ImportError:
    pytest.skip("debugpy not installed", allow_module_level=True)

sys.path.insert(0, "python")
from pydevd_plugins.extensions.types.pydevd_plugin_dims import DimsShapeStr


@pytest.fixture
def provider() -> DimsShapeStr:
    """Create a DimsShapeStr instance for testing.

    Returns:
        DimsShapeStr: A fresh provider instance.

    """
    return DimsShapeStr()


def test_can_provide_numpy_array(provider: DimsShapeStr) -> None:
    """Test that provider accepts numpy arrays."""
    arr = np.array([1, 2, 3])

    result = provider.can_provide(type(arr), type(arr).__name__)

    assert result is True


def test_can_provide_list(provider: DimsShapeStr) -> None:
    """Test that provider accepts lists."""
    lst = [1, 2, 3]

    result = provider.can_provide(type(lst), type(lst).__name__)

    assert result is True


def test_can_provide_dict(provider: DimsShapeStr) -> None:
    """Test that provider accepts dicts."""
    d = {"a": 1, "b": 2}

    result = provider.can_provide(type(d), type(d).__name__)

    assert result is True


def test_can_provide_tuple(provider: DimsShapeStr) -> None:
    """Test that provider accepts tuples."""
    t = (1, 2, 3)

    result = provider.can_provide(type(t), type(t).__name__)

    assert result is True


def test_can_provide_set(provider: DimsShapeStr) -> None:
    """Test that provider accepts sets."""
    s = {1, 2, 3}

    result = provider.can_provide(type(s), type(s).__name__)

    assert result is True


def test_cannot_provide_string(provider: DimsShapeStr) -> None:
    """Test that provider rejects strings to avoid noise."""
    s = "hello"

    result = provider.can_provide(type(s), type(s).__name__)

    assert result is False


def test_get_str_numpy_array_1d(provider: DimsShapeStr) -> None:
    """Test shape display for 1D numpy array."""
    arr = np.array([1, 2, 3])

    result = provider.get_str(arr)

    assert result.startswith("{[3]}")
    assert "[1 2 3]" in result


def test_get_str_numpy_array_2d(provider: DimsShapeStr) -> None:
    """Test shape display for 2D numpy array."""
    arr = np.array([[1, 2, 3], [4, 5, 6]])

    result = provider.get_str(arr)

    assert result.startswith("{[2, 3]}")


def test_get_str_numpy_array_3d(provider: DimsShapeStr) -> None:
    """Test shape display for 3D numpy array."""
    arr = np.zeros((2, 3, 4))

    result = provider.get_str(arr)

    assert result.startswith("{[2, 3, 4]}")


def test_get_str_list(provider: DimsShapeStr) -> None:
    """Test length display for list."""
    lst = [1, 2, 3, 4, 5]

    result = provider.get_str(lst)

    assert result.startswith("{5}")
    assert "[1, 2, 3, 4, 5]" in result


def test_get_str_dict(provider: DimsShapeStr) -> None:
    """Test length display for dict."""
    d = {"a": 1, "b": 2}

    result = provider.get_str(d)

    assert result.startswith("{2}")


def test_get_str_tuple(provider: DimsShapeStr) -> None:
    """Test length display for tuple."""
    t = (1, 2, 3)

    result = provider.get_str(t)

    assert result.startswith("{3}")
    assert "(1, 2, 3)" in result


def test_get_str_set(provider: DimsShapeStr) -> None:
    """Test length display for set."""
    s = {1, 2, 3, 4}

    result = provider.get_str(s)

    assert result.startswith("{4}")


def test_get_str_empty_list(provider: DimsShapeStr) -> None:
    """Test length display for empty list."""
    lst = []

    result = provider.get_str(lst)

    assert result.startswith("{0}")


def test_get_str_nested_list(provider: DimsShapeStr) -> None:
    """Test length display for nested list shows outer length."""
    lst = [[1, 2], [3, 4], [5, 6]]

    result = provider.get_str(lst)

    assert result.startswith("{3}")


def test_get_str_exception_handling(provider: DimsShapeStr) -> None:
    """Test that exceptions in get_str are handled gracefully."""
    mock_obj = Mock()
    mock_obj.shape = Mock(side_effect=Exception("Test exception"))

    result = provider.get_str(mock_obj)

    assert isinstance(result, str)
    assert "Mock" in result or "<" in result


@pytest.mark.skipif("torch" not in sys.modules, reason="PyTorch not installed")
def test_can_provide_torch_tensor(provider: DimsShapeStr) -> None:
    """Test that provider accepts PyTorch tensors."""
    import torch

    tensor = torch.tensor([1, 2, 3])

    result = provider.can_provide(type(tensor), type(tensor).__name__)

    assert result is True


@pytest.mark.skipif("torch" not in sys.modules, reason="PyTorch not installed")
def test_get_str_torch_tensor_1d(provider: DimsShapeStr) -> None:
    """Test shape display for 1D PyTorch tensor."""
    import torch

    tensor = torch.tensor([1.0, 2.0, 3.0])

    result = provider.get_str(tensor)

    assert result.startswith("{[3]}")


@pytest.mark.skipif("torch" not in sys.modules, reason="PyTorch not installed")
def test_get_str_torch_tensor_2d(provider: DimsShapeStr) -> None:
    """Test shape display for 2D PyTorch tensor."""
    import torch

    tensor = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

    result = provider.get_str(tensor)

    assert result.startswith("{[2, 3]}")


@pytest.mark.skipif("torch" not in sys.modules, reason="PyTorch not installed")
def test_get_str_torch_tensor_3d(provider: DimsShapeStr) -> None:
    """Test shape display for 3D PyTorch tensor."""
    import torch

    tensor = torch.zeros(2, 3, 4)

    result = provider.get_str(tensor)

    assert result.startswith("{[2, 3, 4]}")


@pytest.mark.skipif("pandas" not in sys.modules, reason="pandas not installed")
def test_can_provide_dataframe(provider: DimsShapeStr) -> None:
    """Test that provider accepts pandas DataFrames."""
    import pandas as pd

    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    result = provider.can_provide(type(df), type(df).__name__)

    assert result is True


@pytest.mark.skipif("pandas" not in sys.modules, reason="pandas not installed")
def test_get_str_dataframe(provider: DimsShapeStr) -> None:
    """Test shape display for pandas DataFrame."""
    import pandas as pd

    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    result = provider.get_str(df)

    assert result.startswith("{[3, 2]}")


@pytest.mark.skipif("pandas" not in sys.modules, reason="pandas not installed")
def test_can_provide_series(provider: DimsShapeStr) -> None:
    """Test that provider accepts pandas Series."""
    import pandas as pd

    series = pd.Series([1, 2, 3, 4, 5])

    result = provider.can_provide(type(series), type(series).__name__)

    assert result is True


@pytest.mark.skipif("pandas" not in sys.modules, reason="pandas not installed")
def test_get_str_series(provider: DimsShapeStr) -> None:
    """Test shape display for pandas Series."""
    import pandas as pd

    series = pd.Series([1, 2, 3, 4, 5])

    result = provider.get_str(series)

    assert result.startswith("{[5]}")
