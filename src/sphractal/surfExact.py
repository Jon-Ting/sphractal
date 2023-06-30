from concurrent.futures import ProcessPoolExecutor as Pool
from math import ceil
from numba import njit
import numpy as np
from os import mkdir
from os.path import isdir

from sphractal.utils import calcDist, oppositeInnerAtoms
# from sphractal.utils import annotate


MIN_VAL_FROM_BOUND = 5.0  # Angstrom


@njit(fastmath=True, cache=True)
def getNearFarCoord(scanBoxIdx, scanBoxLen, lowBound, atomCoord):
    """Find the nearest and furthest point of a given box from a given atom."""
    scanBoxMax = lowBound - MIN_VAL_FROM_BOUND + (scanBoxIdx+1)*scanBoxLen
    scanBoxMin = scanBoxMax - scanBoxLen
    if atomCoord < scanBoxMin:
        scanBoxNear, scanBoxFar = scanBoxMin, scanBoxMax
    elif atomCoord > scanBoxMax:
        scanBoxNear, scanBoxFar = scanBoxMax, scanBoxMin
    else:
        scanBoxNear = atomCoord
        # The farthest point is always a corner
        scanBoxFar = scanBoxMin if scanBoxMax-atomCoord < scanBoxLen/2 else scanBoxMax
    return scanBoxNear, scanBoxFar


@njit(fastmath=True, cache=True)
def scanBox(minXYZ, scanBoxIdxs, scanBoxNearFarXYZs, scanBoxLen,
            atomIdx, atomRad, atomXYZ, atomNeighIdxs,
            atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
            rmInSurf=True):
    """Find the nearest and furthest point of a given box from a given atom."""
    # Remove the box if it covers the inner surface
    if rmInSurf:
        scanBoxX = minXYZ[0] - MIN_VAL_FROM_BOUND + (scanBoxIdxs[0]+1)*scanBoxLen - scanBoxLen*0.5
        scanBoxY = minXYZ[1] - MIN_VAL_FROM_BOUND + (scanBoxIdxs[1]+1)*scanBoxLen - scanBoxLen*0.5
        scanBoxZ = minXYZ[2] - MIN_VAL_FROM_BOUND + (scanBoxIdxs[2]+1)*scanBoxLen - scanBoxLen*0.5
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
    magnFac, scanBoxLen, minXYZ, atomIdx, atomRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, rmInSurf = args
    atomXYZ, atomNeighIdxsPadded = atomsXYZ[atomIdx], atomsNeighIdxs[atomIdx]
    atomNeighIdxs = atomNeighIdxsPadded[atomNeighIdxsPadded > -1]

    atomX, atomY, atomZ = atomXYZ
    minX, minY, minZ = minXYZ
    atomBoxIdxX = int((atomX - minX + MIN_VAL_FROM_BOUND)/scanBoxLen)
    atomBoxIdxY = int((atomY - minY + MIN_VAL_FROM_BOUND)/scanBoxLen)
    atomBoxIdxZ = int((atomZ - minZ + MIN_VAL_FROM_BOUND)/scanBoxLen)
    numScan = ceil((atomRad + scanBoxLen)/scanBoxLen)
    atomSurfBoxs, atomBulkBoxs = [], []
    for i in range(-numScan, numScan + 1):
        scanBoxIdxX = atomBoxIdxX + i
        if scanBoxIdxX < 0 or scanBoxIdxX >= magnFac:
            continue
        scanBoxNearX, scanBoxFarX = getNearFarCoord(scanBoxIdxX, scanBoxLen, minX, atomX)
        for j in range(-numScan, numScan + 1):
            scanBoxIdxY = atomBoxIdxY + j
            if scanBoxIdxY < 0 or scanBoxIdxY >= magnFac:
                continue
            scanBoxNearY, scanBoxFarY = getNearFarCoord(scanBoxIdxY, scanBoxLen, minY, atomY)
            for k in range(-numScan, numScan + 1):
                scanBoxIdxZ = atomBoxIdxZ + k
                if scanBoxIdxZ < 0 or scanBoxIdxZ >= magnFac:
                    continue
                scanBoxNearZ, scanBoxFarZ = getNearFarCoord(scanBoxIdxZ, scanBoxLen, minZ, atomZ)

                belong = scanBox(minXYZ, (scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ),
                                 (scanBoxNearX, scanBoxNearY, scanBoxNearZ, scanBoxFarX, scanBoxFarY, scanBoxFarZ),
                                 scanBoxLen,
                                 atomIdx, atomRad, atomXYZ, atomNeighIdxs,
                                 atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                 rmInSurf)
                if belong == 'surf':
                    atomSurfBoxs.append((scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ))
                elif belong == 'bulk':
                    atomBulkBoxs.append((scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ))
    return atomSurfBoxs, atomBulkBoxs


# @annotate('scanAtomsForLoop', color='cyan')
@njit(fastmath=True, cache=True)
def scanAtomsForLoop(atomsIdxs, magnFac, scanBoxLen, minXYZ,
                     atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                     rmInSurf=True):
    """Serialised loop to scan the atoms for timing comparison with the parallelised version."""
    allAtomsSurfBoxs, allAtomsBulkBoxs = [], []
    for atomIdx in atomsIdxs:
        scanAtomInp = (magnFac, scanBoxLen, minXYZ, atomIdx,
                       atomsRad[atomIdx], atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, rmInSurf)
        atomSurfBoxs, atomBulkBoxs = scanAtom(scanAtomInp)
        allAtomsSurfBoxs.extend(atomSurfBoxs)
        allAtomsBulkBoxs.extend(atomBulkBoxs)
    return allAtomsSurfBoxs, allAtomsBulkBoxs


# @annotate('scanAllAtoms', color='magenta')
def scanAllAtoms(args):
    """Count the number of boxes that cover the outer spherical surface of a set of atoms for a given box size."""
    magnFac, scanBoxLen, atomsIdxs, minXYZ, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, rmInSurf, verbose = args
    scanAtomInps = [(magnFac, scanBoxLen, minXYZ, atomIdx, atomsRad[atomIdx],
                     atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, rmInSurf) for atomIdx in atomsIdxs]
    allAtomsSurfBoxs, allAtomsBulkBoxs = [], []
    with Pool() as pool:
        for scanAtomResult in pool.map(scanAtom, scanAtomInps):
            allAtomsSurfBoxs.extend(scanAtomResult[0])
            allAtomsBulkBoxs.extend(scanAtomResult[1])
    # allAtomsSurfBoxs, allAtomsBulkBoxs = scanAtomsForLoop(atomsIdxs, magnFac, scanBoxLen, minXYZ,
    #                                                         atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
    #                                                         rmInSurf)
    allAtomsSurfBoxs, allAtomsBulkBoxs = set(allAtomsSurfBoxs), set(allAtomsBulkBoxs)
    allAtomsSurfBoxs.difference_update(allAtomsBulkBoxs)

    if verbose:
        epsInvStr = f"{1 / scanBoxLen:.2f}"
        print(f"{epsInvStr.rjust(10)}{str(len(allAtomsBulkBoxs)).rjust(12)}{str(len(allAtomsSurfBoxs)).rjust(12)}")
    return allAtomsSurfBoxs, allAtomsBulkBoxs


# @annotate('writeBoxCoords', color='yellow')
def writeBoxCoords(atomsEle, atomsXYZ, allSurfBoxs, allBulkBoxs, minXYZ, scanBoxLens,
                   writeFileDir, npName):
    """Write out coordinates of scanned boxes."""
    minX, minY, minZ = minXYZ
    boxCoordsDir = f"{writeFileDir}/boxCoords"
    if not isdir(boxCoordsDir):
        if not isdir(writeFileDir):
            mkdir(writeFileDir)
        mkdir(boxCoordsDir)
    with open(f"{boxCoordsDir}/{npName}_boxCoords.xyz", 'w') as f:
        for (i, scanBoxLen) in enumerate(scanBoxLens):
            if i != 0:
                f.write('\n')
            f.write(f"{len(atomsEle) + len(allSurfBoxs[i]) + len(allBulkBoxs[i])}\n")
            for (j, atomXYZ) in enumerate(atomsXYZ):
                f.write(f"\n{atomsEle[j]}\t{atomXYZ[0]} {atomXYZ[1]} {atomXYZ[2]}")
            for (boxIDX, boxIDY, boxIDZ) in allSurfBoxs[i]:
                boxX = minX - MIN_VAL_FROM_BOUND + boxIDX*scanBoxLen + scanBoxLen/2
                boxY = minY - MIN_VAL_FROM_BOUND + boxIDY*scanBoxLen + scanBoxLen/2
                boxZ = minZ - MIN_VAL_FROM_BOUND + boxIDZ*scanBoxLen + scanBoxLen/2
                f.write(f"\nOV\t{boxX:.6f} {boxY:.6f} {boxZ:.6f}")
            for (boxIDX, boxIDY, boxIDZ) in allBulkBoxs[i]:
                boxX = minX - MIN_VAL_FROM_BOUND + boxIDX*scanBoxLen + scanBoxLen/2
                boxY = minY - MIN_VAL_FROM_BOUND + boxIDY*scanBoxLen + scanBoxLen/2
                boxZ = minZ - MIN_VAL_FROM_BOUND + boxIDZ*scanBoxLen + scanBoxLen/2
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
