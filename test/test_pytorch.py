"""
Test script for PyTorch tensor shape display.

To test:
1. Install PyTorch: pip install torch
2. Install the dims extension in VSCode
3. Set a breakpoint on any line below
4. Start debugging this file
5. Check the Variables view - you should see shape info for tensors

Expected output in Variables view:
- tensor_2d: {[2, 3]}, tensor([[1., 2., 3.], [4., 5., 6.]])
- tensor_3d: {[2, 3, 4]}, tensor([[[...]]])
"""

try:
    import torch

    # Test PyTorch tensors
    tensor_2d = torch.tensor([[1., 2., 3.], [4., 5., 6.]])
    tensor_3d = torch.zeros(2, 3, 4)

    # Test with different data types
    int_tensor = torch.randint(0, 10, (5, 5))
    float_tensor = torch.randn(3, 4)

    print("Set a breakpoint and debug to see dims in action!")
    print(f"Tensor shape: {tensor_2d.shape}")

except ImportError:
    print("PyTorch not installed. Install with: pip install torch")
