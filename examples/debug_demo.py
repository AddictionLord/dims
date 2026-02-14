"""
Manual debugging demo script for dims extension.

Usage:
1. Install the dims extension in VSCode
2. Set breakpoints on lines below
3. Start debugging this file (F5)
4. Check the Variables view - you should see shape info

Expected output in Variables view:
- arr_2d: {[2, 3]}, array([[1, 2, 3], [4, 5, 6]])
- my_list: {5}, [1, 2, 3, 4, 5]
- my_dict: {2}, {'a': 1, 'b': 2}
"""

import numpy as np

# NumPy arrays with .shape attribute
arr_1d = np.array([1, 2, 3, 4, 5])
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
arr_3d = np.zeros((2, 3, 4))

# Standard Python collections
my_list = [1, 2, 3, 4, 5]
nested_list = [[1, 2], [3, 4], [5, 6]]
my_dict = {'a': 1, 'b': 2}
my_set = {1, 2, 3, 4}
my_tuple = (1, 2, 3)

# Strings should NOT show length (to avoid noise)
my_string = "hello world"

# Set a breakpoint here and inspect variables
print(f"Array shape: {arr_2d.shape}")
print(f"List length: {len(my_list)}")
print("Check the Variables view in the debugger!")
