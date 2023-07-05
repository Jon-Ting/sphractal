from concurrent.futures import ProcessPoolExecutor as Pool
from math import sqrt
from os import mkdir
from os.path import isdir

from itertools import product
import numpy as np

from sphractal.constants import ATOMIC_RAD_DICT
from sphractal.utils import ceil, oppositeInnerAtoms


MIN_VAL_FROM_BOUND = 5.0  # Angstrom
NUM_SCAN_THRESH_MP = 27


def getNearFarCoord(scanBoxIdx, scanBoxLen, lowBound, atomCoord):
    """Find the nearest and furthest point of box scanBoxIdx from atomCoord."""
    scanBoxMax = lowBound - MIN_VAL_FROM_BOUND + (scanBoxIdx + 1) * scanBoxLen
    scanBoxMin = scanBoxMax - scanBoxLen
    if atomCoord < scanBoxMin:
        scanBoxNear, scanBoxFar = scanBoxMin, scanBoxMax
    elif atomCoord > scanBoxMax:
        scanBoxNear, scanBoxFar = scanBoxMax, scanBoxMin
    else:
        scanBoxNear = atomCoord
        # The farthest point is always a corner
        scanBoxFar = scanBoxMin if scanBoxMax - atomCoord < scanBoxLen / 2 else scanBoxMax
    return scanBoxNear, scanBoxFar


def scanBoxConc(atomBoxIdxs, scanBoxDirections, magnFac, scanBoxLen, minXYZ, atom, atoms,
                rmInSurf=True):
    """
    Check whether a given box covers a given atom's outer spherical surface.
    TODO: Check whether it's working, Add the algorithm to remove inner surface
    """
    belong = None
    scanBoxIdxX = atomBoxIdxs[0] + scanBoxDirections[0]
    scanBoxIdxY = atomBoxIdxs[1] + scanBoxDirections[1]
    scanBoxIdxZ = atomBoxIdxs[2] + scanBoxDirections[2]
    scanBoxIdxs = (scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ)
    if any(i < 0 or i >= magnFac for i in scanBoxIdxs):
        return
    minX, minY, minZ = minXYZ
    scanBoxNearX, scanBoxFarX = getNearFarCoord(scanBoxIdxX, scanBoxLen, minXYZ[0], atom.X)
    scanBoxNearY, scanBoxFarY = getNearFarCoord(scanBoxIdxY, scanBoxLen, minXYZ[1], atom.Y)
    scanBoxNearZ, scanBoxFarZ = getNearFarCoord(scanBoxIdxZ, scanBoxLen, minXYZ[2], atom.Z)

    if rmInSurf:
        scanBoxX = minX - MIN_VAL_FROM_BOUND + (scanBoxIdxX + 1) * scanBoxLen - scanBoxLen * 0.5
        scanBoxY = minY - MIN_VAL_FROM_BOUND + (scanBoxIdxY + 1) * scanBoxLen - scanBoxLen * 0.5
        scanBoxZ = minZ - MIN_VAL_FROM_BOUND + (scanBoxIdxZ + 1) * scanBoxLen - scanBoxLen * 0.5
        if not oppositeInnerAtoms(np.array((scanBoxX, scanBoxY, scanBoxZ)), atom, atoms):
            return belong, scanBoxIdxs 

    distNear = sqrt((atom.X - scanBoxNearX) ** 2 + (atom.Y - scanBoxNearX) ** 2 + (atom.Z - scanBoxNearZ) ** 2)
    distFar = sqrt((atom.X - scanBoxFarX) ** 2 + (atom.Y - scanBoxFarY) ** 2 + (atom.Z - scanBoxFarZ) ** 2)
    atomRad = ATOMIC_RAD_DICT[atom.ele]
    if not atom.isSurf:
        if distNear < atomRad < distFar or distFar < atomRad:
            belong = 'bulk'
    else:
        if distNear < atomRad < distFar:
            belong = 'surf'
        elif distFar < atomRad:
            belong = 'bulk'
    return belong, scanBoxIdxs


def scanBoxNestedNoCheck(minXYZ, scanBoxIdxs, scanBoxNearFarXYZs, scanBoxLen, atom, atomRad,
                         atoms,
                         rmInSurf=True):
    belong = None
    minX, minY, minZ = minXYZ
    scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ = scanBoxIdxs
    scanBoxNearX, scanBoxNearY, scanBoxNearZ, scanBoxFarX, scanBoxFarY, scanBoxFarZ = scanBoxNearFarXYZs

    if rmInSurf:
        scanBoxX = minX - MIN_VAL_FROM_BOUND + (scanBoxIdxX + 1) * scanBoxLen - scanBoxLen * 0.5
        scanBoxY = minY - MIN_VAL_FROM_BOUND + (scanBoxIdxY + 1) * scanBoxLen - scanBoxLen * 0.5
        scanBoxZ = minZ - MIN_VAL_FROM_BOUND + (scanBoxIdxZ + 1) * scanBoxLen - scanBoxLen * 0.5
        if not oppositeInnerAtoms(np.array((scanBoxX, scanBoxY, scanBoxZ)), atom, atoms):
            return belong, scanBoxIdxs

    distNear = sqrt(
        (atom.X - scanBoxNearX) ** 2 + (atom.Y - scanBoxNearY) ** 2 + (atom.Z - scanBoxNearZ) ** 2)
    distFar = sqrt(
        (atom.X - scanBoxFarX) ** 2 + (atom.Y - scanBoxFarY) ** 2 + (atom.Z - scanBoxFarZ) ** 2)
    if not atom.isSurf:
        if distNear < atomRad < distFar or distFar < atomRad:
            belong = 'bulk'
    else:
        if distNear < atomRad < distFar:
            belong = 'surf'
        elif distFar < atomRad:
            belong = 'bulk'
    return belong, scanBoxIdxs


def scanBoxNested(minXYZ, scanBoxIdxs, scanBoxNearFarXYZs, scanBoxLen, atom, atomRad,
                  surfBoxes, bulkBoxes,  
                  atoms,
                  rmInSurf=True):
    minX, minY, minZ = minXYZ
    scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ = scanBoxIdxs
    scanBoxNearX, scanBoxNearY, scanBoxNearZ, scanBoxFarX, scanBoxFarY, scanBoxFarZ = scanBoxNearFarXYZs
    if rmInSurf:
        scanBoxX = minX - MIN_VAL_FROM_BOUND + (scanBoxIdxX + 1) * scanBoxLen - scanBoxLen * 0.5
        scanBoxY = minY - MIN_VAL_FROM_BOUND + (scanBoxIdxY + 1) * scanBoxLen - scanBoxLen * 0.5
        scanBoxZ = minZ - MIN_VAL_FROM_BOUND + (scanBoxIdxZ + 1) * scanBoxLen - scanBoxLen * 0.5
        if not oppositeInnerAtoms(np.array((scanBoxX, scanBoxY, scanBoxZ)), atom, atoms):
            return
    # Shorter but slower alternative
    # scanBoxDirs = [scanBoxDir for scanBoxDir in product(range(-numScan, numScan + 1), repeat=3)]
    # for scanBoxDir in scanBoxDirs:
    #     scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ = atomBoxIdxX + scanBoxDir[0], \
    #         atomBoxIdxY + scanBoxDir[1], atomBoxIdxZ + scanBoxDir[2]
    #     if any(l < 0 or l >= magnFac for l in (scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ)): continue
    #     scanBoxNearX, scanBoxFarX = getNearFarCoord(scanBoxIdxX, scanBoxLen, minX, atom.X)
    #     scanBoxNearY, scanBoxFarY = getNearFarCoord(scanBoxIdxY, scanBoxLen, minY, atom.Y)
    #     scanBoxNearZ, scanBoxFarZ = getNearFarCoord(scanBoxIdxZ, scanBoxLen, minZ, atom.Z)
    distNear = sqrt(
        (atom.X - scanBoxNearX) ** 2 + (atom.Y - scanBoxNearY) ** 2 + (atom.Z - scanBoxNearZ) ** 2)
    distFar = sqrt(
        (atom.X - scanBoxFarX) ** 2 + (atom.Y - scanBoxFarY) ** 2 + (atom.Z - scanBoxFarZ) ** 2)
    if not atom.isSurf:
        if distNear < atomRad < distFar or distFar < atomRad:
            if scanBoxIdxs in bulkBoxes:
                return
            elif scanBoxIdxs in surfBoxes:
                surfBoxes.remove(scanBoxIdxs)
                bulkBoxes.add(scanBoxIdxs)
            else:
                bulkBoxes.add(scanBoxIdxs)
    else:  # For surface atom
        if distNear < atomRad < distFar:
            if scanBoxIdxs in bulkBoxes or scanBoxIdxs in surfBoxes:
                return
            else:
                surfBoxes.add(scanBoxIdxs)
        elif distFar < atomRad:
            if scanBoxIdxs in bulkBoxes:
                return
            elif scanBoxIdxs in surfBoxes:
                surfBoxes.remove(scanBoxIdxs)
                bulkBoxes.add(scanBoxIdxs)
            else:
                bulkBoxes.add(scanBoxIdxs)
    return surfBoxes, bulkBoxes


def scanAtom(magnFac, scanBoxLen, minXYZ, atom,
             atoms,
             atomSurfBoxes, atomBulkBoxes,
             rmInSurf=True,
             boxConc=True):
    """
    Count the boxes that cover the outer spherical surface of a given atom.
    TODO: Transform xyz coordinates when reading into atoms to prevent using minXYZ repetitively.
    """
    minX, minY, minZ = minXYZ
    atomBoxIdxX = int((atom.X - minX + MIN_VAL_FROM_BOUND) / scanBoxLen)
    atomBoxIdxY = int((atom.Y - minY + MIN_VAL_FROM_BOUND) / scanBoxLen)
    atomBoxIdxZ = int((atom.Z - minZ + MIN_VAL_FROM_BOUND) / scanBoxLen)
    atomRad = ATOMIC_RAD_DICT[atom.ele]
    numScan = ceil((atomRad + scanBoxLen) / scanBoxLen)
    # boxConc = True if numScan > NUM_SCAN_THRESH_MP else False  # TODO: covered input argument (argument to be removed)
    if boxConc:
        scanBoxInp = [((atomBoxIdxX, atomBoxIdxY, atomBoxIdxZ), scanBoxDirection, magnFac, scanBoxLen,
                       minXYZ, atom, atoms, rmInSurf) for scanBoxDirection in
                      product(range(-numScan, numScan + 1), repeat=3)]
        with Pool() as pool:
            for scanBoxResult in pool.starmap(scanBoxConc, scanBoxInp):
                if scanBoxResult[0] == 'surf':
                    atomSurfBoxes.add(scanBoxResult[1])
                elif scanBoxResult[0] == 'bulk':
                    atomBulkBoxes.add(scanBoxResult[1])
    else:
        for i in range(-numScan, numScan + 1):
            scanBoxIdxX = atomBoxIdxX + i
            if scanBoxIdxX < 0 or scanBoxIdxX >= magnFac:
                continue
            scanBoxNearX, scanBoxFarX = getNearFarCoord(scanBoxIdxX, scanBoxLen, minX, atom.X)
            for j in range(-numScan, numScan + 1):
                scanBoxIdxY = atomBoxIdxY + j
                if scanBoxIdxY < 0 or scanBoxIdxY >= magnFac:
                    continue
                scanBoxNearY, scanBoxFarY = getNearFarCoord(scanBoxIdxY, scanBoxLen, minY, atom.Y)
                for k in range(-numScan, numScan + 1):
                    scanBoxIdxZ = atomBoxIdxZ + k
                    if scanBoxIdxZ < 0 or scanBoxIdxZ >= magnFac:
                        continue
                    scanBoxNearZ, scanBoxFarZ = getNearFarCoord(scanBoxIdxZ, scanBoxLen, minZ, atom.Z)

                    scanBoxIdxs = (scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ)
                    scanBoxNearFarXYZs = (scanBoxNearX, scanBoxNearY, scanBoxNearZ,
                                          scanBoxFarX, scanBoxFarY, scanBoxFarZ)
                    scanBoxResult = scanBoxNested(minXYZ, scanBoxIdxs, scanBoxNearFarXYZs,
                                                  scanBoxLen, atom, atomRad,
                                                  atomSurfBoxes, atomBulkBoxes, 
                                                  atoms,
                                                  rmInSurf)
                    if scanBoxResult:
                        atomSurfBoxes, atomBulkBoxes = scanBoxResult

    return atomSurfBoxes, atomBulkBoxes


def scanAllAtoms(magnFac, scanBoxLen, targetAtoms, minXYZ,
                 allAtoms,
                 rmInSurf=True, verbose=False,
                 atomConc=True, boxConc=True):  # TODO: atomConc, boxConc, etc to be removed eventually
    """Count the boxes that cover the outer spherical surface of a set of atoms for a given box size."""
    allAtomsSurfBoxes, allAtomsBulkBoxes = set(), set()
    if atomConc:
        scanAtomInp = [(magnFac, scanBoxLen, minXYZ, atom,
                        allAtoms,
                        allAtomsSurfBoxes, allAtomsBulkBoxes, 
                        rmInSurf,
                        boxConc) for atom in targetAtoms]
        with Pool() as pool:
            for scanAtomResult in pool.starmap(scanAtom, scanAtomInp):
                allAtomsSurfBoxes.update(scanAtomResult[0])
                allAtomsBulkBoxes.update(scanAtomResult[1])
        allAtomsSurfBoxes.difference_update(allAtomsBulkBoxes)
    else:
        for atom in targetAtoms:
            allAtomsSurfBoxes, allAtomsBulkBoxes = scanAtom(magnFac, scanBoxLen, minXYZ, atom,
                                                            allAtoms,
                                                            allAtomsSurfBoxes, allAtomsBulkBoxes,
                                                            rmInSurf,
                                                            boxConc)

    if verbose:
        print(f"\tMagnification, Counts (bulk, surf):\t{magnFac} {len(allAtomsBulkBoxes)} {len(allAtomsSurfBoxes)}")
    return allAtomsSurfBoxes, allAtomsBulkBoxes


def writeBoxCoords(atoms, allSurfBoxes, allBulkBoxes, minXYZ, scanBoxLens,
                   writeFileDir, npName):
    """Write out coordinates of scanned boxes."""
    minX, minY, minZ = minXYZ
    boxCoordsDir = f"{writeFileDir}/boxCoords"
    if not isdir(boxCoordsDir):
        mkdir(boxCoordsDir)
    with open(f"{boxCoordsDir}/{npName}_boxCoords.xyz", 'w') as f:
        for (i, scanBoxLen) in enumerate(scanBoxLens):
            if i != 0:
                f.write('\n')
            f.write(f"{len(atoms) + len(allSurfBoxes[i]) + len(allBulkBoxes[i])}\n")
            for atom in atoms:
                f.write(f"\n{atom.ele}\t{atom.X} {atom.Y} {atom.Z}")
            for (boxIDX, boxIDY, boxIDZ) in allSurfBoxes[i]:
                boxX = minX - MIN_VAL_FROM_BOUND + boxIDX * scanBoxLen + scanBoxLen / 2
                boxY = minY - MIN_VAL_FROM_BOUND + boxIDY * scanBoxLen + scanBoxLen / 2
                boxZ = minZ - MIN_VAL_FROM_BOUND + boxIDZ * scanBoxLen + scanBoxLen / 2
                f.write(f"\nOV\t{boxX:.6f} {boxY:.6f} {boxZ:.6f}")
            for (boxIDX, boxIDY, boxIDZ) in allBulkBoxes[i]:
                boxX = minX - MIN_VAL_FROM_BOUND + boxIDX * scanBoxLen + scanBoxLen / 2
                boxY = minY - MIN_VAL_FROM_BOUND + boxIDY * scanBoxLen + scanBoxLen / 2
                boxZ = minZ - MIN_VAL_FROM_BOUND + boxIDZ * scanBoxLen + scanBoxLen / 2
                f.write(f"\nIV\t{boxX:.6f} {boxY:.6f} {boxZ:.6f}")


def findTargetAtoms(atoms, rmInSurf=True):
    targetAtoms = []
    for atom in atoms:
        if rmInSurf:
            if atom.isSurf:
                targetAtoms.append(atom)
        else:
            if sum(tuple(atoms[neighIdx].isSurf for neighIdx in atom.neighs)) > 0:
                targetAtoms.append(atom)
    return targetAtoms
