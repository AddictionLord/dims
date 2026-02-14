import logging
from typing import Dict, List, Set, Tuple

import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

arr_1d: npt.NDArray[np.int_] = np.array([1, 2, 3, 4, 5])
arr_2d: npt.NDArray[np.int_] = np.array([[1, 2, 3], [4, 5, 6]])
arr_3d: npt.NDArray[np.float64] = np.zeros((2, 3, 4))

my_list: List[int] = [1, 2, 3, 4, 5]
nested_list: List[List[int]] = [[1, 2], [3, 4], [5, 6]]
my_dict: Dict[str, int] = {"a": 1, "b": 2}
my_set: Set[int] = {1, 2, 3, 4}
my_tuple: Tuple[int, int, int] = (1, 2, 3)

my_string: str = "hello world"

logger.info("Array shape: %s", arr_2d.shape)
logger.info("List length: %d", len(my_list))
logger.info("Check the Variables view in the debugger!")
