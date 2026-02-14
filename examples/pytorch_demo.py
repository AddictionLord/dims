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

try:
    import torch

    # PyTorch tensors with .shape attribute
    tensor_1d = torch.tensor([1., 2., 3., 4., 5.])
    tensor_2d = torch.tensor([[1., 2., 3.], [4., 5., 6.]])
    tensor_3d = torch.zeros(2, 3, 4)

    # Different data types
    int_tensor = torch.randint(0, 10, (5, 5))
    float_tensor = torch.randn(3, 4)

    # Set a breakpoint here and inspect variables
    print(f"Tensor shape: {tensor_2d.shape}")
    print("Check the Variables view in the debugger!")

except ImportError:
    print("PyTorch not installed. Install with: pip install torch")
