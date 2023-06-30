from math import cos, pi, sin, sqrt
from numba import njit
import numpy as np
from os import mkdir
from os.path import isdir

from sphractal.constants import ATOMIC_RAD_DICT, METALLIC_RAD_DICT
from sphractal.utils import calcDist, oppositeInnerAtoms
# from sphractal.utils import annotate


@njit(fastmath=True, cache=True)
def fibonacciSphere(numPoint, sphereRad):
    """Generate evenly spread points on the surface of a sphere with a specified radius."""
    xyzs = np.empty((numPoint, 3), dtype=np.float64)
    phi = pi * (sqrt(5)-1)  # Golden angle (radians)
    for i in range(numPoint):
        y = 1 - (i / float(numPoint-1))*2  # y \in [1, -1]
        radius = sqrt(1 - y*y)  # Radius at y
        theta = phi * i  # Golden angle increment
        x = cos(theta) * radius
        z = sin(theta) * radius
        xyzs[i] = (x * sphereRad, y * sphereRad, z * sphereRad)
    return xyzs


@njit(fastmath=True, cache=True)
def withinNeighRad(surfPointXYZ, atomNeighIdxs, atomsRad, atomsXYZ):
    """Return whether a surface point generated around a given atom falls within the radius of a neighbouring atom."""
    for neighIdx in atomNeighIdxs:
        if calcDist(atomsXYZ[neighIdx], surfPointXYZ) <= atomsRad[neighIdx]:
            return True
    return False


# @annotate('pointsOnAtom', color='cyan')
@njit(fastmath=True, cache=True)
def pointsOnAtom(atomIdx, numPoint, atomsSurfIdxs, atomsRad, atomsXYZ, atomsNeighIdxs, surfPoints=None, rmInSurf=True):
    """Generate surface points around an atom and classify them as either inner or outer surface."""
    if surfPoints is None:
        surfPoints = fibonacciSphere(numPoint, atomsRad[atomIdx])
    atomXYZ, atomNeighIdxsPadded = atomsXYZ[atomIdx], atomsNeighIdxs[atomIdx]
    atomNeighIdxs = atomNeighIdxsPadded[atomNeighIdxsPadded > -1]
    outerSurfs, innerSurfs = [], []
    for surfPoint in surfPoints:
        surfPointXYZ = surfPoint + atomXYZ
        if withinNeighRad(surfPointXYZ, atomNeighIdxs, atomsRad, atomsXYZ):
            continue
        if (not rmInSurf) or (rmInSurf and oppositeInnerAtoms(surfPointXYZ, atomXYZ,
                                                              atomNeighIdxs, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs)):
            outerSurfs.append(surfPointXYZ)
        else:
            innerSurfs.append(surfPointXYZ)
    return outerSurfs, innerSurfs


# @annotate('pointsToVoxels', color='magenta')
@njit(fastmath=True, cache=True)
def pointsToVoxels(pointXYZs, gridSize):
    """Turn coordinates of point clouds into coordinates of occupied voxels."""
    # Get segmenting points in 3D space
    rangeXYZ = np.array([pointXYZs[:, i].max() - pointXYZs[:, i].min() for i in range(3)])
    maxRange = max(rangeXYZ)
    minXYZs, maxXYZs, segmentXYZs = np.empty(3), np.empty(3), np.empty((3, gridSize + 1))
    for i in range(3):
        minXYZs[i] = pointXYZs[:, i].min() - (maxRange-rangeXYZ[i]) * 0.5
        maxXYZs[i] = pointXYZs[:, i].max() + (maxRange-rangeXYZ[i]) * 0.5
        segmentXYZs[i] = np.linspace(minXYZs[i], maxXYZs[i], num=gridSize+1)

    # Get the index of the segment that each point lies within
    voxelXs = np.clip(np.searchsorted(segmentXYZs[0], pointXYZs[:, 0]) - 1, 0, gridSize)
    voxelYs = np.clip(np.searchsorted(segmentXYZs[1], pointXYZs[:, 1]) - 1, 0, gridSize)
    voxelZs = np.clip(np.searchsorted(segmentXYZs[2], pointXYZs[:, 2]) - 1, 0, gridSize)

    # Get indices of occupied voxels after flattened
    voxelIdxs = set(voxelXs*gridSize*gridSize + voxelYs*gridSize + voxelZs)
    return np.column_stack((voxelXs, voxelYs, voxelZs)), voxelIdxs


# @annotate('writeSurfVoxelIdxs', color='yellow')
def writeSurfVoxelIdxs(writeFileDir, voxelIdxs):
    """Generate a txt file required for 3D box-counting using C++ code written by Ruiz de Miras and Posadas."""
    with open(f"{writeFileDir}/surfVoxelIdxs.txt", 'w') as f:
        for idx in voxelIdxs:
            f.write(f"{idx}\n")


# @annotate('writePCD', color='yellow')
def writePCD(writeFileDir, npName, surfPointXYZs):
    """Generate a pcd file required for 3D box-counting using MATLAB code written by Kazuaki Iida."""
    surfPointsDir = f"{writeFileDir}/surfPoints"
    if not isdir(surfPointsDir):
        if not isdir(writeFileDir):
            mkdir(writeFileDir)
        mkdir(surfPointsDir)
    with open(f"{surfPointsDir}/{npName}_surfPoints.pcd", 'w') as f:
        f.write('# .PCD v.7 - Point Cloud Data file format\nVERSION .7')
        f.write('\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\n')
        f.write(f"WIDTH {len(surfPointXYZs)}\nHEIGHT 1\nPOINTS {len(surfPointXYZs)}\nDATA ascii\n")
        for xyz in surfPointXYZs:
            f.write(f"{xyz[0]} {xyz[1]} {xyz[2]}\n")


# @annotate('writeSurfPoints', color='blue')
def writeSurfPoints(writeFileDir, npName, atomsSurfIdxs, atomsXYZ, surfPointXYZs, nonSurfPointXYZs):
    """Generate an xyz file for visualisation of classified point clouds."""
    surfPointsDir = f"{writeFileDir}/surfPoints"
    if not isdir(surfPointsDir):
        if not isdir(writeFileDir):
            mkdir(writeFileDir)
        mkdir(surfPointsDir)
    with open(f"{surfPointsDir}/{npName}_surfPoints.xyz", 'w') as f:
        f.write(f"{len(surfPointXYZs) + len(nonSurfPointXYZs) + len(atomsSurfIdxs)}\n\n")
        for (i, xyz) in enumerate(surfPointXYZs):
            f.write(f"OU {xyz[0]} {xyz[1]} {xyz[2]} {i}\n")
        for (i, xyz) in enumerate(nonSurfPointXYZs):
            f.write(f"IN {xyz[0]} {xyz[1]} {xyz[2]} {i}\n")
        for atomIdx in atomsSurfIdxs:
            xyz = atomsXYZ[atomIdx]
            f.write(f"SU {xyz[0]} {xyz[1]} {xyz[2]} {atomIdx}\n")


# @annotate('writeSurfVoxels', color='green')
def writeSurfVoxels(writeFileDir, npName, surfVoxelXYZs):
    """Generate an xyz file useful for visualisation of computed surface voxels."""
    surfVoxelsDir = f"{writeFileDir}/surfVoxels"
    if not isdir(surfVoxelsDir):
        if not isdir(writeFileDir):
            mkdir(writeFileDir)
        mkdir(surfVoxelsDir)
    with open(f"{surfVoxelsDir}/{npName}_surfVoxels.xyz", 'w') as f:
        f.write(f"{len(surfVoxelXYZs)}\n\n")
        for (i, xyz) in enumerate(surfVoxelXYZs):
            f.write(f"VX {xyz[0]} {xyz[1]} {xyz[2]} {i}\n")


# @annotate('getSurfPoints', color='cyan')
def genSurfPoints(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                  npName, writeFileDir, 
                  radType='atomic', numPoint=300, gridNum=1024,
                  rmInSurf=True, vis=False, verbose=False, genPCD=False):
    """Generate point clouds approximating the outer spherical surface formed by a set of atoms."""
    # Avoid repeating generation of surface points around atoms with the same radii
    radDict = ATOMIC_RAD_DICT if radType == 'atomic' else METALLIC_RAD_DICT
    surfPointsEles = {atomEle: fibonacciSphere(numPoint, radDict[atomEle]) for atomEle in set(atomsEle)}

    # Generate point clouds and convert to voxels
    surfPointXYZs, nonSurfPointXYZs = [], []
    for atomIdx in atomsSurfIdxs:
        outerSurfs, innerSurfs = pointsOnAtom(atomIdx, numPoint,
                                              atomsSurfIdxs, atomsRad, atomsXYZ, atomsNeighIdxs,
                                              surfPoints=surfPointsEles[atomsEle[atomIdx]],
                                              rmInSurf=rmInSurf)
        surfPointXYZs.extend(outerSurfs)
        nonSurfPointXYZs.extend(innerSurfs)
    surfVoxelXYZs, surfVoxelIdxs = pointsToVoxels(np.array(surfPointXYZs), gridNum)

    # Generate output files
    writeSurfVoxelIdxs(writeFileDir, surfVoxelIdxs)
    if verbose:
        print(f"    {len(surfPointXYZs)} surface points -> {len(surfVoxelIdxs)} voxels, # grids: {gridNum}")
    if genPCD:
        writePCD(writeFileDir, npName, surfPointXYZs)
    if vis:
        writeSurfPoints(writeFileDir, npName, atomsSurfIdxs, atomsXYZ, surfPointXYZs, nonSurfPointXYZs)
        writeSurfVoxels(writeFileDir, npName, surfVoxelXYZs)
