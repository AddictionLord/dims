import os
import sys

import debugpy

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYDEVD_ROOT = os.path.join(os.path.dirname(debugpy.__file__), "_vendored", "pydevd")

sys.path.insert(0, PYDEVD_ROOT)
sys.path.append(os.path.join(REPO_ROOT, "python"))
