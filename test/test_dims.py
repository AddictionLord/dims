"""
Test script to verify dims extension functionality.

To test:
1. Install the dims extension in VSCode
2. Set a breakpoint on any line below
3. Start debugging this file
4. Check the Variables view - you should see shape info prepended to arrays/lists

Expected output in Variables view:
- arr_2d: {[2, 3]}, array([[1, 2, 3], [4, 5, 6]])
- my_list: {5}, [1, 2, 3, 4, 5]
- my_dict: {2}, {'a': 1, 'b': 2}
"""

import numpy as np

# Test NumPy arrays
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
arr_3d = np.zeros((2, 3, 4))

# Test lists
my_list = [1, 2, 3, 4, 5]
nested_list = [[1, 2], [3, 4], [5, 6]]

# Test dicts
my_dict = {'a': 1, 'b': 2}

# Test sets
my_set = {1, 2, 3, 4}

# Test tuples
my_tuple = (1, 2, 3)

# Test strings (should NOT show length)
my_string = "hello world"

print("Set a breakpoint and debug to see dims in action!")
print(f"Array shape: {arr_2d.shape}")
print(f"List length: {len(my_list)}")
