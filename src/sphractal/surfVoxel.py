from math import cos, log10, pi, sin, sqrt
from os import mkdir, system
from os.path import isdir

from numba import njit
import numpy as np

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
def writeSurfVoxelIdxs(outDir, voxelIdxs):
    """Generate a txt file required for 3D box-counting using C++ code written by Ruiz de Miras and Posadas."""
    with open(f"{outDir}/surfVoxelIdxs.txt", 'w') as f:
        for idx in voxelIdxs:
            f.write(f"{idx}\n")


# @annotate('writePCD', color='yellow')
def writePCD(outDir, npName, surfPointXYZs):
    """Generate a pcd file required for 3D box-counting using MATLAB code written by Kazuaki Iida."""
    surfPointsDir = f"{outDir}/surfPoints"
    if not isdir(surfPointsDir):
        if not isdir(outDir):
            mkdir(outDir)
        mkdir(surfPointsDir)
    with open(f"{surfPointsDir}/{npName}_surfPoints.pcd", 'w') as f:
        f.write('# .PCD v.7 - Point Cloud Data file format\nVERSION .7')
        f.write('\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\n')
        f.write(f"WIDTH {len(surfPointXYZs)}\nHEIGHT 1\nPOINTS {len(surfPointXYZs)}\nDATA ascii\n")
        for xyz in surfPointXYZs:
            f.write(f"{xyz[0]} {xyz[1]} {xyz[2]}\n")


# @annotate('writeSurfPoints', color='blue')
def writeSurfPoints(outDir, npName, atomsSurfIdxs, atomsXYZ, surfPointXYZs, nonSurfPointXYZs):
    """Generate an xyz file for visualisation of classified point clouds."""
    surfPointsDir = f"{outDir}/surfPoints"
    if not isdir(surfPointsDir):
        if not isdir(outDir):
            mkdir(outDir)
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
def writeSurfVoxels(outDir, npName, surfVoxelXYZs):
    """Generate an xyz file useful for visualisation of computed surface voxels."""
    surfVoxelsDir = f"{outDir}/surfVoxels"
    if not isdir(surfVoxelsDir):
        if not isdir(outDir):
            mkdir(outDir)
        mkdir(surfVoxelsDir)
    with open(f"{surfVoxelsDir}/{npName}_surfVoxels.xyz", 'w') as f:
        f.write(f"{len(surfVoxelXYZs)}\n\n")
        for (i, xyz) in enumerate(surfVoxelXYZs):
            f.write(f"VX {xyz[0]} {xyz[1]} {xyz[2]} {i}\n")


# @annotate('getSurfPoints', color='cyan')
def genSurfPoints(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                  npName, outDir, 
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
    writeSurfVoxelIdxs(outDir, surfVoxelIdxs)
    if verbose:
        print(f"    {len(surfPointXYZs)} surface points -> {len(surfVoxelIdxs)} voxels, # grids: {gridNum}")
    if genPCD:
        writePCD(outDir, npName, surfPointXYZs)
    if vis:
        writeSurfPoints(outDir, npName, atomsSurfIdxs, atomsXYZ, surfPointXYZs, nonSurfPointXYZs)
        writeSurfVoxels(outDir, npName, surfVoxelXYZs)


# @annotate('voxelBoxCnts', color='blue')
def voxelBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                 npName, outDir='boxCntOutputs', exePath='$FASTBC_EXE',
                 radType='atomic', numPoint=300, gridNum=1024,
                 rmInSurf=True, vis=True, verbose=False, genPCD=False):
    """
    Count the boxes that cover the outer surface of a set of overlapping spheres represented as point clouds for
    different box sizes, using 3D box-counting algorithm written by Ruiz de Miras et al. in C++. 

    IMPORTANT: Make sure the source code has been downloaded from https://github.com/Jon-Ting/fastBC and compiled 
    on your machine. 'exePath' should point to the right directory if FASTBC_EXE is not set as an environment variable.
    
    Parameters
    ----------
    atomsEle : 1D ndarray
        Element type of each atom.
    atomsRad : 1D ndarray
        Radius of each atom.
    atomsSurfIdxs : 1D ndarray
        Indices of surface atoms.
    atomsXYZ : 2D ndarray
        Cartesian coordinates of each atom.
    atomsNeighIdxs : 2D ndarray
        Neighbour atoms indices of each atom.
    npName : str
        Identifier of the measured object, which forms part of the output file name, ideally unique.
    outDir : str, optional
        Path to the directory to store the output files.
    exePath : str, optional
        Path to the compiled C++ executable for box-counting.
    radType : {'atomic', 'metallic'}, optional
        Type of radii to use for the spheres.
    numPoint : int, optional
        Number of surface points to be generated around each atom.
    gridNum : int, optional
        Resolution of the 3D binary image.
    rmInSurf : bool, optional
        Whether to remove the surface points on the inner surface.
    vis : bool, optional
        Whether to generate output files for visualisation.
    verbose : bool
        Whether to display the details.
    genPCD : bool, optional
        Whether to generate pcd file for box-counting using MATLAB code written by Kazuaki Iida.
    
    Returns
    -------
    scales : list
        Box lengths.
    counts : list
        Number of boxes that cover the surface of interest, as represented by the voxels in the 3D binary image.

    Examples
    --------
    >>> eles, rads, xyzs, _, minxyz, maxxyz = readInp('example.xyz')
    >>> neighs, _ = findNN(rads, xyzs, minxyz, maxxyz, 2.5)
    >>> surfs = findSurf(xyzs, neighs, 'alphaShape', 5.0)
    >>> scalesPC, countsPC = voxelBoxCnts(eles, rads, surfs, xyzs, neighs, 'example')

    Notes
    -----
    The 3D binary image resolution (gridNum) is restricted by RAM size available, the relationship is illustrated below:
    -  1024 ->    2 GB (laptops -> typically 8 GB)
    -  2048 ->   16 GB (HPC nodes with GPUs like NCI Gadi gpuvolta queue -> max 32 GB/node)
    -  4096 ->  128 GB
    -  8192 -> 1024 GB (HPC node with huge memories like NCI Gadi megamem queue -> max 2990 GB/node)
    - 16384 -> 8192 GB
    Further details about maximum grid size and memory estimation could be found in 'test.cpp' documented by the authors 
    (https://www.ugr.es/~demiras/fbc/). As a reference, when 8192 grids are used, allocation of memory took 25 min;
    while the CPU algorithm runs for 18 min.
    """
    if verbose:
        print(f"  Approximating the surface with {numPoint} point clouds for each atom...")
    if not isdir(outDir):
        mkdir(outDir)

    genSurfPoints(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                  npName, outDir,
                  radType, numPoint, gridNum,
                  rmInSurf, vis, verbose, genPCD)
    system(f"{exePath} {gridNum} {outDir}/surfVoxelIdxs.txt {outDir}/surfVoxelBoxCnts.txt")
    scales, counts = [], []
    with open(f"{outDir}/surfVoxelBoxCnts.txt", 'r') as f:
        for line in f:
            scales.append(log10(1 / int(line.split()[0])))
            counts.append(log10(int(line.split()[1])))
    return scales[::-1], counts[::-1]
