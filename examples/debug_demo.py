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

from typing import List, Dict, Set, Tuple
import logging
import numpy as np
import numpy.typing as npt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# NumPy arrays with .shape attribute
arr_1d: npt.NDArray[np.int_] = np.array([1, 2, 3, 4, 5])
arr_2d: npt.NDArray[np.int_] = np.array([[1, 2, 3], [4, 5, 6]])
arr_3d: npt.NDArray[np.float64] = np.zeros((2, 3, 4))

# Standard Python collections
my_list: List[int] = [1, 2, 3, 4, 5]
nested_list: List[List[int]] = [[1, 2], [3, 4], [5, 6]]
my_dict: Dict[str, int] = {'a': 1, 'b': 2}
my_set: Set[int] = {1, 2, 3, 4}
my_tuple: Tuple[int, int, int] = (1, 2, 3)

# Strings should NOT show length (to avoid noise)
my_string: str = "hello world"

# Set a breakpoint here and inspect variables
logging.info("Array shape: %s", arr_2d.shape)
logging.info("List length: %d", len(my_list))
logging.info("Check the Variables view in the debugger!")
