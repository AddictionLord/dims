"""
Tests for the dims pydevd plugin.

These tests verify that the DimsShapeStr presentation provider
correctly formats shape information for various Python objects.
"""

import sys
import os
import pytest
import numpy as np
from unittest.mock import Mock


# Add debugpy's vendored pydevd to path so _pydevd_bundle is available
try:
    import debugpy
    debugpy_path = os.path.join(os.path.dirname(debugpy.__file__), '_vendored', 'pydevd')
    sys.path.insert(0, debugpy_path)
except ImportError:
    pytest.skip("debugpy not installed", allow_module_level=True)

# Import the plugin module
sys.path.insert(0, 'python')
from pydevd_plugins.extensions.types.pydevd_plugin_dims import DimsShapeStr


class TestDimsShapeStr:
    """Test suite for DimsShapeStr presentation provider."""

    @pytest.fixture
    def provider(self):
        """Create a DimsShapeStr instance for testing."""
        return DimsShapeStr()

    def test_can_provide_numpy_array(self, provider):
        """Test that provider accepts numpy arrays."""
        arr = np.array([1, 2, 3])
        assert provider.can_provide(type(arr), type(arr).__name__)

    def test_can_provide_list(self, provider):
        """Test that provider accepts lists."""
        lst = [1, 2, 3]
        assert provider.can_provide(type(lst), type(lst).__name__)

    def test_can_provide_dict(self, provider):
        """Test that provider accepts dicts."""
        d = {'a': 1, 'b': 2}
        assert provider.can_provide(type(d), type(d).__name__)

    def test_can_provide_tuple(self, provider):
        """Test that provider accepts tuples."""
        t = (1, 2, 3)
        assert provider.can_provide(type(t), type(t).__name__)

    def test_can_provide_set(self, provider):
        """Test that provider accepts sets."""
        s = {1, 2, 3}
        assert provider.can_provide(type(s), type(s).__name__)

    def test_cannot_provide_string(self, provider):
        """Test that provider rejects strings to avoid noise."""
        s = "hello"
        assert not provider.can_provide(type(s), type(s).__name__)

    def test_get_str_numpy_array_1d(self, provider):
        """Test shape display for 1D numpy array."""
        arr = np.array([1, 2, 3])
        result = provider.get_str(arr)
        assert result.startswith('{[3]}')
        assert '[1 2 3]' in result

    def test_get_str_numpy_array_2d(self, provider):
        """Test shape display for 2D numpy array."""
        arr = np.array([[1, 2, 3], [4, 5, 6]])
        result = provider.get_str(arr)
        assert result.startswith('{[2, 3]}')

    def test_get_str_numpy_array_3d(self, provider):
        """Test shape display for 3D numpy array."""
        arr = np.zeros((2, 3, 4))
        result = provider.get_str(arr)
        assert result.startswith('{[2, 3, 4]}')

    def test_get_str_list(self, provider):
        """Test length display for list."""
        lst = [1, 2, 3, 4, 5]
        result = provider.get_str(lst)
        assert result.startswith('{5}')
        assert '[1, 2, 3, 4, 5]' in result

    def test_get_str_dict(self, provider):
        """Test length display for dict."""
        d = {'a': 1, 'b': 2}
        result = provider.get_str(d)
        assert result.startswith('{2}')

    def test_get_str_tuple(self, provider):
        """Test length display for tuple."""
        t = (1, 2, 3)
        result = provider.get_str(t)
        assert result.startswith('{3}')
        assert '(1, 2, 3)' in result

    def test_get_str_set(self, provider):
        """Test length display for set."""
        s = {1, 2, 3, 4}
        result = provider.get_str(s)
        assert result.startswith('{4}')

    def test_get_str_empty_list(self, provider):
        """Test length display for empty list."""
        lst = []
        result = provider.get_str(lst)
        assert result.startswith('{0}')

    def test_get_str_nested_list(self, provider):
        """Test length display for nested list."""
        lst = [[1, 2], [3, 4], [5, 6]]
        result = provider.get_str(lst)
        assert result.startswith('{3}')  # Outer list length

    def test_get_str_exception_handling(self, provider):
        """Test that exceptions in get_str are handled gracefully."""
        # Create a mock object that has .shape but raises on access
        mock_obj = Mock()
        mock_obj.shape = Mock(side_effect=Exception("Test exception"))

        # Should not raise, should fallback to str(val)
        result = provider.get_str(mock_obj)
        assert isinstance(result, str)
        # Mock objects have a default string representation
        assert 'Mock' in result or '<' in result


@pytest.mark.skipif(
    'torch' not in sys.modules,
    reason="PyTorch not installed"
)
class TestDimsShapeStrPyTorch:
    """Test suite for PyTorch tensor support."""

    @pytest.fixture
    def provider(self):
        """Create a DimsShapeStr instance for testing."""
        return DimsShapeStr()

    def test_can_provide_torch_tensor(self, provider):
        """Test that provider accepts PyTorch tensors."""
        import torch
        tensor = torch.tensor([1, 2, 3])
        assert provider.can_provide(type(tensor), type(tensor).__name__)

    def test_get_str_torch_tensor_1d(self, provider):
        """Test shape display for 1D PyTorch tensor."""
        import torch
        tensor = torch.tensor([1., 2., 3.])
        result = provider.get_str(tensor)
        assert result.startswith('{[3]}')

    def test_get_str_torch_tensor_2d(self, provider):
        """Test shape display for 2D PyTorch tensor."""
        import torch
        tensor = torch.tensor([[1., 2., 3.], [4., 5., 6.]])
        result = provider.get_str(tensor)
        assert result.startswith('{[2, 3]}')

    def test_get_str_torch_tensor_3d(self, provider):
        """Test shape display for 3D PyTorch tensor."""
        import torch
        tensor = torch.zeros(2, 3, 4)
        result = provider.get_str(tensor)
        assert result.startswith('{[2, 3, 4]}')


@pytest.mark.skipif(
    'pandas' not in sys.modules,
    reason="pandas not installed"
)
class TestDimsShapeStrPandas:
    """Test suite for pandas DataFrame support."""

    @pytest.fixture
    def provider(self):
        """Create a DimsShapeStr instance for testing."""
        return DimsShapeStr()

    def test_can_provide_dataframe(self, provider):
        """Test that provider accepts pandas DataFrames."""
        import pandas as pd
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        assert provider.can_provide(type(df), type(df).__name__)

    def test_get_str_dataframe(self, provider):
        """Test shape display for pandas DataFrame."""
        import pandas as pd
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        result = provider.get_str(df)
        # DataFrame has shape attribute
        assert result.startswith('{[3, 2]}')

    def test_can_provide_series(self, provider):
        """Test that provider accepts pandas Series."""
        import pandas as pd
        series = pd.Series([1, 2, 3, 4, 5])
        assert provider.can_provide(type(series), type(series).__name__)

    def test_get_str_series(self, provider):
        """Test shape display for pandas Series."""
        import pandas as pd
        series = pd.Series([1, 2, 3, 4, 5])
        result = provider.get_str(series)
        # Series has shape attribute
        assert result.startswith('{[5]}')
