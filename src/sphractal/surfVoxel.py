from concurrent.futures import ProcessPoolExecutor as Pool
from math import ceil, cos, log10, pi, sin, sqrt
from multiprocessing import cpu_count
from os import mkdir, system
from os.path import isdir

from numba import njit
import numpy as np

from sphractal.constants import ATOMIC_RAD_DICT, METALLIC_RAD_DICT
from sphractal.utils import calcDist, oppositeInnerAtoms
# from sphractal.utils import annotate


@njit(fastmath=True, cache=True)
def fibonacciSphere(numPoints, sphereRad):
    """Generate evenly spread points on the surface of a sphere with a specified radius."""
    xyzs = np.empty((numPoints, 3), dtype=np.float64)
    phi = pi * (sqrt(5)-1)  # Golden angle (radians)
    for i in range(numPoints):
        y = 1 - (i / float(numPoints-1))*2  # y \in [1, -1]
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


@njit(fastmath=True, cache=True)
def rmPoint(args):
    """Check whether a point falls on the outer surface."""
    surfPoint, atomXYZ, atomNeighIdxs, atomsRad, atomsXYZ, rmInSurf, atomsSurfIdxs, atomsNeighIdxs = args
    surfPointXYZ = surfPoint + atomXYZ
    if withinNeighRad(surfPointXYZ, atomNeighIdxs, atomsRad, atomsXYZ):
        return 'isWithinRad', surfPointXYZ
    if (not rmInSurf) or (rmInSurf and oppositeInnerAtoms(surfPointXYZ, atomXYZ,
                                                          atomNeighIdxs, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs)):
        return 'toExclude', surfPointXYZ
    return 'toInclude', surfPointXYZ


# @annotate('pointsOnAtom', color='cyan')
def pointsOnAtom(args):
    """Generate surface points around an atom and classify them as either inner or outer surface."""
    atomIdx, numPoints, atomsSurfIdxs, atomsRad, atomsXYZ, atomsNeighIdxs, maxCPU, surfPoints, rmInSurf = args
    if surfPoints is None:
        surfPoints = fibonacciSphere(numPoints, atomsRad[atomIdx])
    atomXYZ, atomNeighIdxsPadded = atomsXYZ[atomIdx], atomsNeighIdxs[atomIdx]
    atomNeighIdxs = atomNeighIdxsPadded[atomNeighIdxsPadded > -1]
    rmPointInp, outerSurfs, innerSurfs = [], [], []

    # Include points that fall on surface of interest
    for surfPoint in surfPoints:
        if maxCPU > 1:
            rmPointInp.append((surfPoint, atomXYZ, atomNeighIdxs, atomsRad, atomsXYZ, rmInSurf, atomsSurfIdxs, atomsNeighIdxs))
            continue
        pointPosition, surfPointXYZ = rmPoint((surfPoint, atomXYZ, atomNeighIdxs, atomsRad, atomsXYZ, rmInSurf, atomsSurfIdxs, atomsNeighIdxs))
        if pointPosition == 'toExclude':
            outerSurfs.append(surfPointXYZ)
        elif pointPosition == 'toInclude':
            innerSurfs.append(surfPointXYZ)

    # Parallel implementation of the point position assessment algorithm
    if maxCPU > 1:
        with Pool(max_workers=maxCPU) as pool:
            for rmPointResult in pool.map(rmPoint, rmPointInp, 
                                          chunksize=ceil(numPoints / maxCPU)):
                if rmPointResult[0] == 'toExclude':
                    outerSurfs.append(rmPointResult[1])
                elif rmPointResult[0] == 'toInclude':
                    innerSurfs.append(rmPointResult[1])

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
                  npName, outDir='outputs', numCPUs=None, 
                  radType='atomic', numPoints=10000, gridNum=1024,
                  rmInSurf=True, vis=False, verbose=False, genPCD=False):
    """Generate point clouds approximating the outer spherical surface formed by a set of atoms."""
    # Avoid repeating generation of surface points around atoms with the same radii
    radDict = ATOMIC_RAD_DICT if radType == 'atomic' else METALLIC_RAD_DICT
    surfPointsEles = {atomEle: fibonacciSphere(numPoints, radDict[atomEle]) for atomEle in set(atomsEle)}

    # Resource allocations
    if numCPUs is None: 
        numCPUs = cpu_count()
    minAtomCPU = max(1, len(atomsSurfIdxs) // 25)
    maxPointCPUperAtom = ceil(numPoints / numPoints)  # ceil(numPoints / 25)
    if numCPUs > maxPointCPUperAtom * minAtomCPU:
        atomConcMaxCPU = numCPUs // maxPointCPUperAtom
        pointConcMaxCPU = maxPointCPUperAtom
    # elif numCPUs > minAtomCPU:
    #     atomConcMaxCPU = minAtomCPU
    #     pointConcMaxCPU = numCPUs // minAtomCPU
    else:
        atomConcMaxCPU, pointConcMaxCPU = numCPUs, 1
    if verbose:
        print(f"    Assessing points over:\n      {len(atomsSurfIdxs)} atoms using {atomConcMaxCPU} cpu(s)...\n"
              f"      {numPoints} points using {pointConcMaxCPU} cpu(s)...")

    # Generate point clouds and convert to voxels
    surfPointXYZs, nonSurfPointXYZs = [], []
    pointsOnAtomInp = []
    for atomIdx in atomsSurfIdxs:
        if atomConcMaxCPU > 1:  # Adjust back
            pointsOnAtomInp.append((atomIdx, numPoints, atomsSurfIdxs, atomsRad, atomsXYZ, atomsNeighIdxs, pointConcMaxCPU,
                                    surfPointsEles[atomsEle[atomIdx]], rmInSurf))
        else:
            outerSurfs, innerSurfs = pointsOnAtom((atomIdx, numPoints, atomsSurfIdxs, atomsRad, atomsXYZ, atomsNeighIdxs, pointConcMaxCPU, surfPointsEles[atomsEle[atomIdx]], rmInSurf))
            surfPointXYZs.extend(outerSurfs)
            nonSurfPointXYZs.extend(innerSurfs)

    # Parallel implementation of the points generation around atoms
    if atomConcMaxCPU > 1:
        with Pool(max_workers=atomConcMaxCPU) as pool:
            for pointsOnAtomResult in pool.map(pointsOnAtom, pointsOnAtomInp, 
                                               chunksize=ceil(len(atomsSurfIdxs) / atomConcMaxCPU)):
                surfPointXYZs.extend(pointsOnAtomResult[0])
                nonSurfPointXYZs.extend(pointsOnAtomResult[1])

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
                 npName, outDir='outputs', numCPUs=None, exePath='$FASTBC',
                 radType='atomic', numPoints=300, gridNum=1024,
                 rmInSurf=True, vis=True, verbose=False, genPCD=False):
    """
    Count the boxes that cover the outer surface of a set of overlapping spheres represented as point clouds for different box sizes, using 3D box-counting algorithm written by Ruiz de Miras et al. in C++. 

    IMPORTANT: Make sure the source code has been downloaded from https://github.com/Jon-Ting/fastBC and compiled on your machine. 'exePath' should point to the right directory if FASTBC is not set as an environment variable.
    
    Parameters
    ----------
    atomsEle : 1D ndarray of strs
        Element type of each atom.
    atomsRad : 1D ndarray of floats
        Radius of each atom.
    atomsSurfIdxs : 1D ndarray of ints
        Indices of surface atoms.
    atomsXYZ : 2D ndarray of floats
        Cartesian coordinates of each atom.
    atomsNeighIdxs : 2D ndarray of ints
        Neighbour atoms indices of each atom.
    npName : str
        Identifier of the measured object, which forms part of the output file name, ideally unique.
    outDir : str, optional
        Path to the directory to store the output files.
    numCPUs : int, optional
        Number of CPUs to be used for parallelisation of tasks.
    exePath : str, optional
        Path to the compiled C++ executable for box-counting.
    radType : {'atomic', 'metallic'}, optional
        Type of radii to use for the spheres.
    numPoints : int, optional
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
    >>> neighs, _ = findNN(rads, xyzs, minxyz, maxxyz, 1.2)
    >>> surfs = findSurf(xyzs, neighs, 'alphaShape', 5.0)
    >>> scalesPC, countsPC = voxelBoxCnts(eles, rads, surfs, xyzs, neighs, 'example')

    Notes
    -----
    The 3D binary image resolution (gridNum) is restricted to 1024 or lower. Details about maximum grid size and memory estimation could be found in 'test.cpp' documented by the authors (https://www.ugr.es/~demiras/fbc/).
    """
    if verbose:
        print(f"  Approximating the surface with {numPoints} points for each atom...")
    if not isdir(outDir):
        mkdir(outDir)

    genSurfPoints(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                  npName, outDir, numCPUs,
                  radType, numPoints, gridNum,
                  rmInSurf, vis, verbose, genPCD)
    system(f"{exePath} {gridNum} {outDir}/surfVoxelIdxs.txt {outDir}/surfVoxelBoxCnts.txt")
    scales, counts = [], []
    with open(f"{outDir}/surfVoxelBoxCnts.txt", 'r') as f:
        for line in f:
            scales.append(log10(1 / int(line.split()[0])))
            counts.append(log10(int(line.split()[1])))
    return scales[::-1], counts[::-1]
