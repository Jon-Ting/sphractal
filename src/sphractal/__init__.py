# Read version from installed package
from importlib.metadata import version
__version__ = version('sphractal')

# Populate package namespace
__all__ = ['constants', 'datasets', 'utils', 'boxCnt']
from sphractal.constants import ATOMIC_RAD_DICT, METALLIC_RAD_DICT
from sphractal.datasets import getExampleDataPath
from sphractal.utils import readXYZ, findNN, findSurf
from sphractal.boxCnt import getVoxelBoxCnts, getSphereBoxCnts, findSlope, runBoxCnt
