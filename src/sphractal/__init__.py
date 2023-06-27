# Read version from installed package
from importlib.metadata import version
__version__ = version('sphractal')

# Populate package namespace
__all__ = ['constants', 'boxCnt']
from sphractal.constants import ATOMIC_RAD_DICT, METALLIC_RAD_DICT
from sphractal.boxCnt import runBoxCnt
