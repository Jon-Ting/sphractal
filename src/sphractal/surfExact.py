from concurrent.futures import ProcessPoolExecutor as Pool
from math import ceil
from os import mkdir
from os.path import isdir

from numba import njit
import numpy as np

from sphractal.utils import calcDist, oppositeInnerAtoms
# from sphractal.utils import annotate


@njit(fastmath=True, cache=True)
def getNearFarCoord(scanBoxIdx, boxLen, lowBound, atomCoord, minValFromBound=5.0):
    """Find the nearest and furthest point of a given box from a given atom."""
    scanBoxMax = lowBound - minValFromBound + (scanBoxIdx+1)*boxLen
    scanBoxMin = scanBoxMax - boxLen
    if atomCoord < scanBoxMin:
        scanBoxNear, scanBoxFar = scanBoxMin, scanBoxMax
    elif atomCoord > scanBoxMax:
        scanBoxNear, scanBoxFar = scanBoxMax, scanBoxMin
    else:
        scanBoxNear = atomCoord
        # The farthest point is always a corner
        scanBoxFar = scanBoxMin if scanBoxMax-atomCoord < boxLen/2 else scanBoxMax
    return scanBoxNear, scanBoxFar


@njit(fastmath=True, cache=True)
def scanBox(minXYZ, scanBoxIdxs, scanBoxNearFarXYZs, boxLen,
            atomIdx, atomRad, atomXYZ, atomNeighIdxs,
            atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
            minValFromBound=5.0, rmInSurf=True):
    """Find the nearest and furthest point of a given box from a given atom."""
    # Remove the box if it covers the inner surface
    if rmInSurf:
        scanBoxX = minXYZ[0] - minValFromBound + (scanBoxIdxs[0]+1)*boxLen - boxLen*0.5
        scanBoxY = minXYZ[1] - minValFromBound + (scanBoxIdxs[1]+1)*boxLen - boxLen*0.5
        scanBoxZ = minXYZ[2] - minValFromBound + (scanBoxIdxs[2]+1)*boxLen - boxLen*0.5
        if not oppositeInnerAtoms(np.array((scanBoxX, scanBoxY, scanBoxZ)), atomXYZ, atomNeighIdxs,
                                  atomsSurfIdxs, atomsXYZ, atomsNeighIdxs):
            return 'none'

    # Check what does the box cover
    distNear = calcDist(atomXYZ, np.array(scanBoxNearFarXYZs[:3]))
    distFar = calcDist(atomXYZ, np.array(scanBoxNearFarXYZs[-3:]))
    if atomIdx in atomsSurfIdxs:
        if distNear < atomRad < distFar:
            return 'surf'
        elif distFar < atomRad:
            return 'bulk'
        else:
            return 'none'
    else:
        if distNear < atomRad < distFar or distFar < atomRad:
            return 'bulk'
        else:
            return 'none'


# @annotate('scanAtom', color='cyan')
@njit(fastmath=True, cache=True)
def scanAtom(args):
    """Count the number of boxes that cover the outer spherical surface of a given atom."""
    magn, boxLen, minXYZ, atomIdx, atomRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, minValFromBound, rmInSurf = args
    atomXYZ, atomNeighIdxsPadded = atomsXYZ[atomIdx], atomsNeighIdxs[atomIdx]
    atomNeighIdxs = atomNeighIdxsPadded[atomNeighIdxsPadded > -1]

    atomX, atomY, atomZ = atomXYZ
    minX, minY, minZ = minXYZ
    atomBoxIdxX = int((atomX - minX + minValFromBound)/boxLen)
    atomBoxIdxY = int((atomY - minY + minValFromBound)/boxLen)
    atomBoxIdxZ = int((atomZ - minZ + minValFromBound)/boxLen)
    numScan = ceil((atomRad + boxLen)/boxLen)
    atomSurfBoxs, atomBulkBoxs = [], []
    for i in range(-numScan, numScan + 1):
        scanBoxIdxX = atomBoxIdxX + i
        if scanBoxIdxX < 0 or scanBoxIdxX >= magn:
            continue
        scanBoxNearX, scanBoxFarX = getNearFarCoord(scanBoxIdxX, boxLen, minX, atomX, minValFromBound)
        for j in range(-numScan, numScan + 1):
            scanBoxIdxY = atomBoxIdxY + j
            if scanBoxIdxY < 0 or scanBoxIdxY >= magn:
                continue
            scanBoxNearY, scanBoxFarY = getNearFarCoord(scanBoxIdxY, boxLen, minY, atomY, minValFromBound)
            for k in range(-numScan, numScan + 1):
                scanBoxIdxZ = atomBoxIdxZ + k
                if scanBoxIdxZ < 0 or scanBoxIdxZ >= magn:
                    continue
                scanBoxNearZ, scanBoxFarZ = getNearFarCoord(scanBoxIdxZ, boxLen, minZ, atomZ, minValFromBound)

                belong = scanBox(minXYZ, (scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ),
                                 (scanBoxNearX, scanBoxNearY, scanBoxNearZ, scanBoxFarX, scanBoxFarY, scanBoxFarZ),
                                 boxLen,
                                 atomIdx, atomRad, atomXYZ, atomNeighIdxs,
                                 atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                 minValFromBound, rmInSurf)
                if belong == 'surf':
                    atomSurfBoxs.append((scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ))
                elif belong == 'bulk':
                    atomBulkBoxs.append((scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ))
    return atomSurfBoxs, atomBulkBoxs


# @annotate('scanAtomsForLoop', color='cyan')
@njit(fastmath=True, cache=True)
def scanAtomsForLoop(atomsIdxs, magn, boxLen, minXYZ,
                     atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                     minValFromBound=5.0, rmInSurf=True):
    """Serialised loop to scan the atoms for timing comparison with the parallelised version."""
    allAtomsSurfBoxs, allAtomsBulkBoxs = [], []
    for atomIdx in atomsIdxs:
        scanAtomInp = (magn, boxLen, minXYZ, atomIdx,
                       atomsRad[atomIdx], atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, 
                       minValFromBound, rmInSurf)
        atomSurfBoxs, atomBulkBoxs = scanAtom(scanAtomInp)
        allAtomsSurfBoxs.extend(atomSurfBoxs)
        allAtomsBulkBoxs.extend(atomBulkBoxs)
    return allAtomsSurfBoxs, allAtomsBulkBoxs


# @annotate('scanAllAtoms', color='magenta')
def scanAllAtoms(args):
    """Count the number of boxes that cover the outer spherical surface of a set of atoms for a given box size."""
    magn, boxLen, atomsIdxs, minXYZ, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, minValFromBound, rmInSurf, verbose, maxCPU = args
    scanAtomInps = [(magn, boxLen, minXYZ, atomIdx, atomsRad[atomIdx],
                     atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, minValFromBound, rmInSurf) for atomIdx in atomsIdxs]
    allAtomsSurfBoxs, allAtomsBulkBoxs = [], []
    with Pool(max_workers=maxCPU) as pool:
        for scanAtomResult in pool.map(scanAtom, scanAtomInps, chunksize=ceil(len(atomsIdxs) / maxCPU)):
            allAtomsSurfBoxs.extend(scanAtomResult[0])
            allAtomsBulkBoxs.extend(scanAtomResult[1])
    # allAtomsSurfBoxs, allAtomsBulkBoxs = scanAtomsForLoop(atomsIdxs, magn, boxLen, minXYZ,
    #                                                       atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
    #                                                       minValFromBound, rmInSurf)
    allAtomsSurfBoxs, allAtomsBulkBoxs = set(allAtomsSurfBoxs), set(allAtomsBulkBoxs)
    allAtomsSurfBoxs.difference_update(allAtomsBulkBoxs)

    if verbose:
        epsInvStr = f"{1 / boxLen:.2f}"
        print(f"{epsInvStr.rjust(10)}{str(len(allAtomsBulkBoxs)).rjust(12)}{str(len(allAtomsSurfBoxs)).rjust(12)}")
    return allAtomsSurfBoxs, allAtomsBulkBoxs


# @annotate('writeBoxCoords', color='yellow')
def writeBoxCoords(atomsEle, atomsXYZ, allSurfBoxs, allBulkBoxs, minXYZ, boxLens, minValFromBound,
                   writeFileDir, npName):
    """Write out coordinates of scanned boxes."""
    minX, minY, minZ = minXYZ
    boxCoordsDir = f"{writeFileDir}/boxCoords"
    if not isdir(boxCoordsDir):
        if not isdir(writeFileDir):
            mkdir(writeFileDir)
        mkdir(boxCoordsDir)
    with open(f"{boxCoordsDir}/{npName}_boxCoords.xyz", 'w') as f:
        for (i, boxLen) in enumerate(boxLens):
            if i != 0:
                f.write('\n')
            f.write(f"{len(atomsEle) + len(allSurfBoxs[i]) + len(allBulkBoxs[i])}\n")
            for (j, atomXYZ) in enumerate(atomsXYZ):
                f.write(f"\n{atomsEle[j]}\t{atomXYZ[0]} {atomXYZ[1]} {atomXYZ[2]}")
            for (boxIDX, boxIDY, boxIDZ) in allSurfBoxs[i]:
                boxX = minX - minValFromBound + boxIDX*boxLen + boxLen/2
                boxY = minY - minValFromBound + boxIDY*boxLen + boxLen/2
                boxZ = minZ - minValFromBound + boxIDZ*boxLen + boxLen/2
                f.write(f"\nOV\t{boxX:.6f} {boxY:.6f} {boxZ:.6f}")
            for (boxIDX, boxIDY, boxIDZ) in allBulkBoxs[i]:
                boxX = minX - minValFromBound + boxIDX*boxLen + boxLen/2
                boxY = minY - minValFromBound + boxIDY*boxLen + boxLen/2
                boxZ = minZ - minValFromBound + boxIDZ*boxLen + boxLen/2
                f.write(f"\nIV\t{boxX:.6f} {boxY:.6f} {boxZ:.6f}")


# @annotate('findTargetAtoms', color='cyan')
@njit(fastmath=True, cache=True)
def findTargetAtoms(atomsNeighIdxs):
    """Find atoms to be scanned if not removing inner surfaces (atoms with neighbours that are on the surface)."""
    atomsIdxs = []
    for (atomIdx, atomNeighIdxs) in enumerate(atomsNeighIdxs):
        if sum(atomNeighIdxs[atomNeighIdxs > -1]) > 0:
            atomsIdxs.append(atomIdx)
    return np.array(atomsIdxs)
