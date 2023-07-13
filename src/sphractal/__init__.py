"""
Sphractal
=========

Provides
    1. Representation of surface of 3D complex objects consisting of spherical entities as 
    either point clouds or exact surfaces.
    2. Efficient algorithms for box-counting calculations.
    3. Customisable parameters to control the level of detail and accuracy of the calculation.

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided with the code, 
and a loose standing reference guide, available from 
`the Sphractal homepage <https://sphractal.readthedocs.io/en/latest/>`_.

Code snippets in docstrings are indicated by three greater-than signs::

  >>> x = 42
  >>> x = x + 1

Use the built-in ``help`` function to view a function's docstring::

  >>> import sphractal
  >>> help(sphractal.runBoxCnt)
  ... # docstring: +SKIP

Utilities
---------
test (To be implemented)
    Run Sphractal tests.
__version__
    Return Sphractal version string.
"""

# Read version from installed package
from importlib.metadata import version
__version__ = version('sphractal')

# Populate package namespace
__all__ = ['constants', 'datasets', 'utils', 'surfVoxel', 'surfExact', 'boxCnt']
from sphractal.constants import ATOMIC_RAD_DICT, METALLIC_RAD_DICT, PLT_PARAMS
from sphractal.datasets import getExampleDataPath, getBenchmarkDataPaths
from sphractal.utils import readInp, findNN, findSurf
from sphractal.surfVoxel import voxelBoxCnts
from sphractal.surfExact import exactBoxCnts
from sphractal.boxCnt import findSlope, runBoxCnt
