"""
PyTorch tensor debugging demo for dims extension.

Usage:
1. Install PyTorch: pip install torch
2. Install the dims extension in VSCode
3. Set breakpoints on lines below
4. Start debugging this file (F5)
5. Check the Variables view - tensors should show shapes

Expected output in Variables view:
- tensor_2d: {[2, 3]}, tensor([[1., 2., 3.], [4., 5., 6.]])
- tensor_3d: {[2, 3, 4]}, tensor([[[...]]])
"""

from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    import torch

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
    import torch
    from torch import Tensor

    # PyTorch tensors with .shape attribute
    tensor_1d: Tensor = torch.tensor([1., 2., 3., 4., 5.])
    tensor_2d: Tensor = torch.tensor([[1., 2., 3.], [4., 5., 6.]])
    tensor_3d: Tensor = torch.zeros(2, 3, 4)

    # Different data types
    int_tensor: Tensor = torch.randint(0, 10, (5, 5))
    float_tensor: Tensor = torch.randn(3, 4)

    # Set a breakpoint here and inspect variables
    logging.info("Tensor shape: %s", tensor_2d.shape)
    logging.info("Check the Variables view in the debugger!")

except ImportError:
    logging.error("PyTorch not installed. Install with: pip install torch")
