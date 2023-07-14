from concurrent.futures import ProcessPoolExecutor as Pool
from math import ceil, log10
from multiprocessing import cpu_count
from os import mkdir
from os.path import isdir

from numba import njit
import numpy as np

from sphractal.utils import calcDist, oppositeInnerAtoms
# from sphractal.utils import annotate


@njit(fastmath=True, cache=True)
def getNearFarCoord(scanBoxIdx, boxLen, lowBound, atomCoord, bufferDist=5.0):
    """Find the nearest and furthest point of a given box from a given atom."""
    scanBoxMax = lowBound - bufferDist + (scanBoxIdx+1)*boxLen
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
            bufferDist=5.0, rmInSurf=True):
    """Find the nearest and furthest point of a given box from a given atom."""
    # Remove the box if it covers the inner surface
    if rmInSurf:
        scanBoxX = minXYZ[0] - bufferDist + (scanBoxIdxs[0]+1)*boxLen - boxLen*0.5
        scanBoxY = minXYZ[1] - bufferDist + (scanBoxIdxs[1]+1)*boxLen - boxLen*0.5
        scanBoxZ = minXYZ[2] - bufferDist + (scanBoxIdxs[2]+1)*boxLen - boxLen*0.5
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
    magn, boxLen, minXYZ, atomIdx, atomRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, bufferDist, rmInSurf = args
    atomXYZ, atomNeighIdxsPadded = atomsXYZ[atomIdx], atomsNeighIdxs[atomIdx]
    atomNeighIdxs = atomNeighIdxsPadded[atomNeighIdxsPadded > -1]

    atomX, atomY, atomZ = atomXYZ
    minX, minY, minZ = minXYZ
    atomBoxIdxX = int((atomX - minX + bufferDist)/boxLen)
    atomBoxIdxY = int((atomY - minY + bufferDist)/boxLen)
    atomBoxIdxZ = int((atomZ - minZ + bufferDist)/boxLen)
    numScan = ceil((atomRad + boxLen)/boxLen)
    atomSurfBoxs, atomBulkBoxs = [], []
    for i in range(-numScan, numScan + 1):
        scanBoxIdxX = atomBoxIdxX + i
        if scanBoxIdxX < 0 or scanBoxIdxX >= magn:
            continue
        scanBoxNearX, scanBoxFarX = getNearFarCoord(scanBoxIdxX, boxLen, minX, atomX, bufferDist)
        for j in range(-numScan, numScan + 1):
            scanBoxIdxY = atomBoxIdxY + j
            if scanBoxIdxY < 0 or scanBoxIdxY >= magn:
                continue
            scanBoxNearY, scanBoxFarY = getNearFarCoord(scanBoxIdxY, boxLen, minY, atomY, bufferDist)
            for k in range(-numScan, numScan + 1):
                scanBoxIdxZ = atomBoxIdxZ + k
                if scanBoxIdxZ < 0 or scanBoxIdxZ >= magn:
                    continue
                scanBoxNearZ, scanBoxFarZ = getNearFarCoord(scanBoxIdxZ, boxLen, minZ, atomZ, bufferDist)

                belong = scanBox(minXYZ, (scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ),
                                 (scanBoxNearX, scanBoxNearY, scanBoxNearZ, scanBoxFarX, scanBoxFarY, scanBoxFarZ),
                                 boxLen,
                                 atomIdx, atomRad, atomXYZ, atomNeighIdxs,
                                 atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                 bufferDist, rmInSurf)
                if belong == 'surf':
                    atomSurfBoxs.append((scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ))
                elif belong == 'bulk':
                    atomBulkBoxs.append((scanBoxIdxX, scanBoxIdxY, scanBoxIdxZ))
    return atomSurfBoxs, atomBulkBoxs


# @annotate('scanAtomsForLoop', color='cyan')
@njit(fastmath=True, cache=True)
def scanAtomsForLoop(atomsIdxs, magn, boxLen, minXYZ,
                     atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                     bufferDist=5.0, rmInSurf=True):
    """Serialised loop to scan the atoms for timing comparison with the parallelised version."""
    allAtomsSurfBoxs, allAtomsBulkBoxs = [], []
    for atomIdx in atomsIdxs:
        scanAtomInp = (magn, boxLen, minXYZ, atomIdx,
                       atomsRad[atomIdx], atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, 
                       bufferDist, rmInSurf)
        atomSurfBoxs, atomBulkBoxs = scanAtom(scanAtomInp)
        allAtomsSurfBoxs.extend(atomSurfBoxs)
        allAtomsBulkBoxs.extend(atomBulkBoxs)
    return allAtomsSurfBoxs, allAtomsBulkBoxs


# @annotate('scanAllAtoms', color='magenta')
def scanAllAtoms(args):
    """Count the number of boxes that cover the outer spherical surface of a set of atoms for a given box size."""
    magn, boxLen, atomsIdxs, minXYZ, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, bufferDist, rmInSurf, verbose, maxCPU = args
    scanAtomInps = [(magn, boxLen, minXYZ, atomIdx, atomsRad[atomIdx],
                     atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, bufferDist, rmInSurf) for atomIdx in atomsIdxs]
    allAtomsSurfBoxs, allAtomsBulkBoxs = [], []
    with Pool(max_workers=maxCPU) as pool:
        for scanAtomResult in pool.map(scanAtom, scanAtomInps, chunksize=ceil(len(atomsIdxs) / maxCPU)):
            allAtomsSurfBoxs.extend(scanAtomResult[0])
            allAtomsBulkBoxs.extend(scanAtomResult[1])
    # allAtomsSurfBoxs, allAtomsBulkBoxs = scanAtomsForLoop(atomsIdxs, magn, boxLen, minXYZ,
    #                                                       atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
    #                                                       bufferDist, rmInSurf)
    allAtomsSurfBoxs, allAtomsBulkBoxs = set(allAtomsSurfBoxs), set(allAtomsBulkBoxs)
    allAtomsSurfBoxs.difference_update(allAtomsBulkBoxs)

    if verbose:
        epsInvStr = f"{1 / boxLen:.2f}"
        print(f"{epsInvStr.rjust(10)}{str(len(allAtomsBulkBoxs)).rjust(12)}{str(len(allAtomsSurfBoxs)).rjust(12)}")
    return allAtomsSurfBoxs, allAtomsBulkBoxs


# @annotate('writeBoxCoords', color='yellow')
def writeBoxCoords(atomsEle, atomsXYZ, allSurfBoxs, allBulkBoxs, minXYZ, boxLens, bufferDist,
                   outDir, npName):
    """Write out coordinates of scanned boxes."""
    minX, minY, minZ = minXYZ
    boxCoordsDir = f"{outDir}/boxCoords"
    if not isdir(boxCoordsDir):
        if not isdir(outDir):
            mkdir(outDir)
        mkdir(boxCoordsDir)
    with open(f"{boxCoordsDir}/{npName}_boxCoords.xyz", 'w') as f:
        for (i, boxLen) in enumerate(boxLens):
            if i != 0:
                f.write('\n')
            f.write(f"{len(atomsEle) + len(allSurfBoxs[i]) + len(allBulkBoxs[i])}\n")
            for (j, atomXYZ) in enumerate(atomsXYZ):
                f.write(f"\n{atomsEle[j]}\t{atomXYZ[0]} {atomXYZ[1]} {atomXYZ[2]}")
            for (boxIDX, boxIDY, boxIDZ) in allSurfBoxs[i]:
                boxX = minX - bufferDist + boxIDX*boxLen + boxLen/2
                boxY = minY - bufferDist + boxIDY*boxLen + boxLen/2
                boxZ = minZ - bufferDist + boxIDZ*boxLen + boxLen/2
                f.write(f"\nOV\t{boxX:.6f} {boxY:.6f} {boxZ:.6f}")
            for (boxIDX, boxIDY, boxIDZ) in allBulkBoxs[i]:
                boxX = minX - bufferDist + boxIDX*boxLen + boxLen/2
                boxY = minY - bufferDist + boxIDY*boxLen + boxLen/2
                boxZ = minZ - bufferDist + boxIDZ*boxLen + boxLen/2
                f.write(f"\nIV\t{boxX:.6f} {boxY:.6f} {boxZ:.6f}")


# @annotate('findTargetAtoms', color='cyan')
@njit(fastmath=True, cache=True)
def findTargetAtoms(atomsNeighIdxs, atomsSurfIdxs):
    """Find atoms to be scanned if not removing inner surfaces (atoms with neighbours that are on the surface)."""
    atomsIdxs = []
    for (atomIdx, atomNeighIdxs) in enumerate(atomsNeighIdxs):
        for neighIdx in atomNeighIdxs:
            if neighIdx < 0:
                break
            if neighIdx in atomsSurfIdxs:
                atomsIdxs.append(atomIdx)
                break
    return np.array(atomsIdxs)


# @annotate('exactBoxCnts', color='blue')
def exactBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                 maxRange, minMaxBoxLens, minXYZ, npName, 
                 outDir='boxCntOutputs', numBoxLen=10, bufferDist=5.0,
                 rmInSurf=True, writeBox=True, verbose=False):
    """
    Count the boxes that cover the outer surface of a set of overlapping spheres represented as exact spheres for
    different box sizes.
    
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
    maxRange : float
        Maximum range among all dimensions of the Cartesian space, defines the borders of the largest box.
    minMaxBoxLens : tuple of floats
        Minimum and maximum box lengths.
    minXYZ : 1D ndarray
        Minimum values of each dimension in the Cartesian space.
    npName : str
        Identifier of the measured object, which forms part of the output file name, ideally unique.
    outDir : str, optional
        Path to the directory to store the output files.
    numBoxLen : int, optional
        Number of box lengths to use for the collection of the box count data, spaced evenly on logarithmic scale.
    bufferDist : Union[int,float]
        Buffer distance from the borders of the largest box in Angstrom.
    rmInSurf : bool, optional
        Whether to remove the surface points on the inner surface.
    writeBox : bool, optional
        Whether to generate output files for visualisation.
    verbose : bool, optional
        Whether to display the details.
    
    Returns
    -------
    scales : list
        Box lengths.
    counts : list
        Number of boxes that cover the exact spherical surface of interest.
    
    Examples
    --------
    >>> eles, rads, xyzs, _, minxyz, maxxyz = readInp('example.xyz')
    >>> neighs, _ = findNN(rads, xyzs, minxyz, maxxyz, 1.2)
    >>> surfs = findSurf(xyzs, neighs, 'alphaShape', 2.0)
    >>> scalesES, countsES = exactBoxCnts(eles, rads, surfs, xyzs, neighs, 100, (0.2, 1), minxyz, 'example')
    """
    atomsIdxs = atomsSurfIdxs if rmInSurf else findTargetAtoms(atomsNeighIdxs, atomsSurfIdxs)
    numCPUs = cpu_count()
    boxLenScanMaxWorkers = ceil(numCPUs * numBoxLen / len(atomsIdxs))
    boxLenConc = False if boxLenScanMaxWorkers < 2 else True
    atomScanMaxWorkers = numCPUs - boxLenScanMaxWorkers if boxLenConc else numCPUs

    if verbose:
        print(f"  Representing the surface by treating each atom as exact spheres...")
        print(f"    Parallelised with {atomScanMaxWorkers} out of {numCPUs} cores for scanning over {len(atomsIdxs)} "
              f"atoms, the rest over {numBoxLen} box lengths...")
        print(f"    (1/eps)    (# bulk)    (# surf)")
    if writeBox:
        if not isdir(outDir):
            mkdir(outDir)

    overallBoxLen = maxRange + bufferDist * 2
    allLensSurfBoxs, allLensBulkBoxs, allLensSurfCnts, allLensBulkCnts = [], [], [], []
    scales, scanBoxLens, scanAllAtomsInps = [], [], []
    approxScanBoxLens = np.geomspace(minMaxBoxLens[1], minMaxBoxLens[0], num=numBoxLen)
    for approxScanBoxLen in approxScanBoxLens:  # Evenly reduced box lengths on log scale
        magnFac = int(overallBoxLen / approxScanBoxLen)
        scanBoxLen = overallBoxLen / magnFac
        scanAllAtomsInp = (magnFac, scanBoxLen, atomsIdxs, minXYZ,
                           atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, bufferDist,
                           rmInSurf, verbose, atomScanMaxWorkers)
        if boxLenConc:
            scanAllAtomsInps.append(scanAllAtomsInp) 
        else:
            scanAllAtomsResult = scanAllAtoms(scanAllAtomsInp) 
            allAtomsSurfBoxs, allAtomsBulkBoxs = scanAllAtomsResult
            allLensSurfBoxs.append(allAtomsSurfBoxs)
            allLensBulkBoxs.append(allAtomsBulkBoxs)
            allLensSurfCnts.append(len(allAtomsSurfBoxs))

        scales.append(log10(magnFac / overallBoxLen))
        scanBoxLens.append(scanBoxLen)

    if boxLenConc:
        with Pool(max_workers=boxLenScanMaxWorkers) as pool:
            for scanAllAtomsResult in pool.map(scanAllAtoms, scanAllAtomsInps,
                                               chunksize=ceil(numBoxLen / boxLenScanMaxWorkers)):
                allAtomsSurfBoxs, allAtomsBulkBoxs = scanAllAtomsResult
                allLensSurfBoxs.append(allAtomsSurfBoxs)
                allLensBulkBoxs.append(allAtomsBulkBoxs)
                allLensSurfCnts.append(len(allAtomsSurfBoxs))
    counts = [log10(sCnt) if sCnt != 0 else np.nan for sCnt in allLensSurfCnts]

    if writeBox:
        writeBoxCoords(atomsEle, atomsXYZ, allLensSurfBoxs, allLensBulkBoxs, minXYZ, scanBoxLens, bufferDist, 
                       outDir, npName)
    return scales, counts

