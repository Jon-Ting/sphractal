from math import ceil, floor, sqrt
from time import time

from numba import njit, prange
from numba.typed import List
import numpy as np
# from nvtx import annotate
from scipy.spatial import ConvexHull, Delaunay
from scipy.spatial._qhull import QhullError

from sphractal.constants import ATOMIC_RAD_DICT, METALLIC_RAD_DICT


def estDuration(func):
    """Return time taken to run a function."""
    def wrap(*arg, **kwargs):
        start = time()
        result = func(*arg, **kwargs)
        end = time()
        duration = end - start
        return result, duration
    return wrap


@njit(fastmath=True, cache=True)
def getMinMaxXYZ(atomsXYZ): 
    """Return the minimum and maximum values of each dimension of a set of coordinates."""
    rowNum, colNum = atomsXYZ.shape
    minXYZ, maxXYZ = np.empty(colNum), np.empty(colNum)
    for col in range(colNum):
        minVal = maxVal = atomsXYZ[0, col]
        for row in range(1, rowNum):
            val = atomsXYZ[row, col]
            minVal, maxVal = min(minVal, val), max(maxVal, val)
        minXYZ[col], maxXYZ[col] = minVal, maxVal
    return max(maxXYZ - minXYZ), minXYZ, maxXYZ


# @annotate('readInp', color='cyan')
def readInp(filePath, radType='atomic'):
    """Parse an xyz or a lmp file."""
    radDict = ATOMIC_RAD_DICT if radType == 'atomic' else METALLIC_RAD_DICT
    atomsEle, atomsRad, atomsXYZ = [], [], []
    numLinesSkip = 9 if '.lmp' in filePath else 2
    with open(filePath, 'r') as f:
        for (i, line) in enumerate(f):
            if i < numLinesSkip:
                continue
            eleXYZ = line.split()
            ele = eleXYZ[-4]
            atomsEle.append(ele)
            atomsRad.append(radDict[ele])
            atomX, atomY, atomZ = float(eleXYZ[-3]), float(eleXYZ[-2]), float(eleXYZ[-1])
            atomsXYZ.append((atomX, atomY, atomZ))
    atomsEle, atomsRad, atomsXYZ = np.array(atomsEle, dtype='U2'), np.array(atomsRad), np.array(atomsXYZ)
    maxRange, minXYZ, maxXYZ = getMinMaxXYZ(atomsXYZ)
    return atomsEle, atomsRad, atomsXYZ, maxRange, minXYZ, maxXYZ


@njit(fastmath=True, cache=True)
def allDirVecs():
    """Return a list of vectors corresponding to the standard 26 directions from a point."""
    dirVecs = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                dirVecs.append((x, y, z))
    return dirVecs


# @annotate('findNN', color='magenta')
@njit(fastmath=True, cache=True)
def findNN(atomsRad, atomsXYZ, minXYZ, maxXYZ, maxAtomRad, radMult=1.2, calcBL=False):
    """
    Compute the nearest neighbour list and average bond length for each atom.

    Parameters
    ----------
    atomsRad : 1D ndarray of floats
        Radius of each atom.
    atomsXYZ : 2D ndarray of floats
        Cartesian coordinates of each atom.
    minXYZ : 1D ndarray of floats
        Minimum values of each dimension in the Cartesian space.
    maxXYZ : 1D ndarray of floats
        Maximum values of each dimension in the Cartesian space.
    maxAtomRad : Union[int,float]
        Maximum value of atomic radius.
    radMult : Union[int,float]
        Multiplier to the atomic radii.
    calcBL : bool, optional
        Whether to compute the average bond length for each atom.

    Returns
    -------
    atomsNeighIdxsPadded : 2D ndarray of ints
        Neighbour atoms indices of each atom, padded with -1 for fixed number of columns.
    atomsAvgBondLen : 1D ndarray of floats
        Average bond lengths for each each.
    """
    (minX, minY, minZ), (maxX, maxY, maxZ) = minXYZ, maxXYZ
    atomsNeighIdxs = [[int(i) for i in range(0)] for _ in range(len(atomsRad))]
    atomsAvgBondLen = np.zeros_like(atomsRad)
    stepSize = maxAtomRad * 2 * radMult
    numX, numY, numZ = max(1, ceil((maxX-minX) / stepSize)), max(1, ceil((maxY-minY) / stepSize)), max(1, ceil((maxZ-minZ) / stepSize))
    boxes = [[[[int(i) for i in range(0)] for _ in range(numZ)] for _ in range(numY)] for _ in range(numX)]
    allDirections = allDirVecs()
    for (i, atom1rad) in enumerate(atomsRad):
        atom1X, atom1Y, atom1Z = atomsXYZ[i]

        x = min(numX - 1, floor((atom1X-minX) / stepSize))
        y = min(numY - 1, floor((atom1Y-minY) / stepSize))
        z = min(numZ - 1, floor((atom1Z-minZ) / stepSize))
        for (dirX, dirY, dirZ) in allDirections:
            if 0 <= x + dirX < numX and 0 <= y + dirY < numY and 0 <= z + dirZ < numZ:
                for j in boxes[x + dirX][y + dirY][z + dirZ]:
                    atom2X, atom2Y, atom2Z = atomsXYZ[j]
                    atom2rad = atomsRad[j]

                    diffX, diffY, diffZ = abs(atom1X - atom2X), abs(atom1Y - atom2Y), abs(atom1Z - atom2Z)
                    sumOfSquares = diffX*diffX + diffY*diffY + diffZ*diffZ
                    if sumOfSquares < ((atom1rad+atom2rad)*radMult) ** 2:
                        atomsNeighIdxs[i].append(j)
                        atomsNeighIdxs[j].append(i)
                        if calcBL:
                            atomsAvgBondLen[i] += sqrt(sumOfSquares)
                            atomsAvgBondLen[j] += sqrt(sumOfSquares)
        boxes[x][y][z].append(i)

    # Turn list of lists into NumPy array padded with -1
    maxNeighNum = max([len(atomNeighIdxs) for atomNeighIdxs in atomsNeighIdxs])
    atomsNeighIdxsPadded = np.full((len(atomsNeighIdxs), maxNeighNum), -1)
    for (i, atomNeighIdx) in enumerate(atomsNeighIdxs):
        atomsNeighIdxsPadded[i][:len(atomNeighIdx)] = atomNeighIdx

    if calcBL:
        for atomID in range(len(atomsRad)):
            atomsAvgBondLen[atomID] /= len(atomsNeighIdxs[atomID])
    return atomsNeighIdxsPadded, atomsAvgBondLen


@njit(fastmath=True, cache=True)
def findTetras(tetraVtxsIdxs, r, alpha):
    """Return tetrahedrons with their circumsphere radii smaller than a specified alpha value."""
    return tetraVtxsIdxs[r < alpha, :]


@njit(fastmath=True, cache=True)
def rmDupTris(tris):
    """Remove triangles that occur twice (internal triangles)."""
    unqTris = []
    for tri in tris:
        if tris.count(tri) == 1:
            unqTris.append(tri)
    return unqTris


# @annotate('alphaShape', color='cyan')
def alphaShape(atomsXYZ, tetraVtxsIdxs, alpha):
    """
    Return points that form the surface using alpha shape algorithm.

    Algorithm modified from https://stackoverflow.com/questions/26303878/alpha-shapes-in-3d
    Radius of the sphere fitting inside the tetrahedral < alpha (http://mathworld.wolfram.com/Circumsphere.html)
    """
    # Find radius of the circumsphere
    tetraVtxs = atomsXYZ[tetraVtxsIdxs]
    norm2 = np.sum(tetraVtxs ** 2, axis=2)[:, :, np.newaxis]
    ones = np.ones((tetraVtxs.shape[0], tetraVtxs.shape[1], 1))
    a = np.linalg.det(np.concatenate((tetraVtxs, ones), axis=2))
    Dx = np.linalg.det(np.concatenate((norm2, tetraVtxs[:, :, [1, 2]], ones), axis=2))
    Dy = np.linalg.det(np.concatenate((norm2, tetraVtxs[:, :, [0, 2]], ones), axis=2))
    Dz = np.linalg.det(np.concatenate((norm2, tetraVtxs[:, :, [0, 1]], ones), axis=2))
    c = np.linalg.det(np.concatenate((norm2, tetraVtxs), axis=2))
    with np.errstate(divide='ignore', invalid='ignore'):
        r = np.sqrt(Dx**2 + Dy**2 + Dz**2 - 4*a*c) / (2*np.abs(a))

    # Find tetrahedrons and triangles
    tetras = findTetras(tetraVtxsIdxs, r, alpha)
    triComb = np.array([(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)])
    tris = tetras[:, triComb].reshape(-1, 3)
    tris = rmDupTris(List(tuple(i) for i in tris))
    return np.unique(np.concatenate(tris))


# @annotate('findSurf', color='yellow')
def findSurf(atomsXYZ, atomsNeighIdxs, option='alphaShape', alpha=3.0, bulkCN=12):
    """
    Return the indices of surface atoms.
    
    Parameters
    ----------
    atomsXYZ : 2D ndarray of floats
        Cartesian coordinates of each atom.
    atomsNeighIdxs : 2D ndarray of ints
        Neighbour atoms indices of each atom.
    option : {'alphaShape', 'convexHull', 'numNeigh'}, optional
        Algorithm to identify the spheres on the surface. 
        'convexHull' tends to identify less surface atoms; 'numNeigh' tends to identify more surface atoms.
        'alphaShape' is a generalisation of 'convexHull'.
    alpha : Union[int, float], optional
        'alpha' for the alpha shape algorithm, only used if 'option' is 'alphaShape'.
    bulkCN : int, optional
        Minimum number of neighbouring atoms for a non-surface atom.
    
    Returns
    -------
    atomsSurfIdxs : 1D ndarray of ints
        Indices of surface atoms.
    
    Notes
    -----
    Other alternatives include:
    - https://dl.acm.org/doi/abs/10.1145/2073304.2073339
    - https://onlinelibrary.wiley.com/doi/pdf/10.1002/jcc.25384
    - https://www.jstage.jst.go.jp/article/tmrsj/45/4/45_115/_article
    """
    atomsSurfIdxs = np.zeros(len(atomsXYZ), dtype=np.bool_)
    if option == 'convexHull':
        for atomIdx in np.array(ConvexHull(atomsXYZ).vertices):
            atomsSurfIdxs[atomIdx] = True
    elif option == 'numNeigh':
        for (atomIdx, atomNeighIdxs) in enumerate(atomsNeighIdxs):
            if len(atomNeighIdxs[atomNeighIdxs > -1]) < bulkCN:
                atomsSurfIdxs[atomIdx] = True
    elif option == 'alphaShape':
        try:
            tetraVtxsIdxs = Delaunay(atomsXYZ).simplices
            for atomIdx in alphaShape(atomsXYZ, tetraVtxsIdxs, alpha):
                atomsSurfIdxs[atomIdx] = True
        except QhullError:
            atomsSurfIdxs = np.full(len(atomsXYZ), True)
    atomsSurfIdxs = np.where(atomsSurfIdxs)[0]
    return atomsSurfIdxs


@njit(fastmath=True, cache=True)
def findAtomNeighs(neighIdxs, atomsSurfIdxs):
    """Divide a list of atomic neighbours into two based on whether they lie on the surface."""
    surfNeighIdxs, bulkNeighIdxs = [], []
    for idx in neighIdxs:
        if idx in atomsSurfIdxs:
            surfNeighIdxs.append(idx)
        else:
            bulkNeighIdxs.append(idx)
    return np.array(surfNeighIdxs, dtype=np.uint32), np.array(bulkNeighIdxs, dtype=np.uint32)


@njit(fastmath=True, cache=True)  # parallel=True slows things down, incompatible with multiprocessing.Pool()
def calcDist(p1, p2):
    """Return Euclidean distance between two points."""
    d = 0
    for i in prange(3):
        d += (p2[i] - p1[i]) ** 2
    return d ** 0.5


@njit(fastmath=True, cache=True)
def getOrdSurfNeighCombs(surfNeighDists, surfNeighIdxs):
    """Compute ID pairs of a set of neighbouring atoms, ordered by distance from a given point."""
    ordSurfNeighIdxs = surfNeighIdxs[np.argsort(surfNeighDists)]
    surfNeighIdxPairs = np.stack(np.triu_indices(len(ordSurfNeighIdxs), k=1), axis=-1)
    return [ordSurfNeighIdxs[idxPair] for idxPair in surfNeighIdxPairs]


@njit(fastmath=True, cache=True)
def closestSurfAtoms(pointXYZ, surfNeighIdxs, atomsXYZ, atomsNeighIdxs):
    """Return two closest surface atom pairs from a given point, that are neighbour of each other."""
    if len(surfNeighIdxs) < 2: 
        return np.array([np.nan]), np.array([np.nan])
    surfNeighXYZs = atomsXYZ[surfNeighIdxs]
    surfNeighDists = np.array([calcDist(pointXYZ, surfNeighXYZ) for surfNeighXYZ in surfNeighXYZs])
    for idxPair in getOrdSurfNeighCombs(surfNeighDists, surfNeighIdxs):
        if idxPair[0] in atomsNeighIdxs[idxPair[1]]:
            return atomsXYZ[idxPair[0]], atomsXYZ[idxPair[1]]
    return np.array([np.nan]), np.array([np.nan])


@njit(fastmath=True, cache=True)
def oppositeInnerAtoms(pointXYZ, atom1XYZ, atomNeighIdxs, 
                       atomsSurfIdxs, atomsXYZ, atomsNeighIdxs):
    """Return whether a point lies opposite of the average coordinates of neighbouring inner atoms of a given atom."""
    surfNeighIdxs, bulkNeighIdxs = findAtomNeighs(atomNeighIdxs, atomsSurfIdxs)
    atom2XYZ, atom3XYZ = closestSurfAtoms(pointXYZ, surfNeighIdxs, atomsXYZ, atomsNeighIdxs)
    innerNeighXYZs = atomsXYZ[bulkNeighIdxs] if len(bulkNeighIdxs) > 0 else atomsXYZ[surfNeighIdxs]
    avgInnerAtomXYZ = np.array([innerNeighXYZs[:, i].mean() for i in range(3)])
    normal = avgInnerAtomXYZ - atom1XYZ if len(atom3XYZ) == 1 else np.cross(atom2XYZ - atom1XYZ, atom3XYZ - atom1XYZ)
    # If the given point is on the opposite side of the surface plane, the sign of products of the dot products will be negative
    return np.dot(normal, avgInnerAtomXYZ - atom1XYZ) * np.dot(normal, pointXYZ - atom1XYZ) < 0
