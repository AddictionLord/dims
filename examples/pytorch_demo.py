import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import torch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

try:
    import torch
    from torch import Tensor

    tensor_1d: Tensor = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
    tensor_2d: Tensor = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    tensor_3d: Tensor = torch.zeros(2, 3, 4)

    int_tensor: Tensor = torch.randint(0, 10, (5, 5))
    float_tensor: Tensor = torch.randn(3, 4)

    logger.info("Tensor shape: %s", tensor_2d.shape)
    logger.info("Check the Variables view in the debugger!")

except ImportError:
    logger.error("PyTorch not installed. Install with: pip install torch")
