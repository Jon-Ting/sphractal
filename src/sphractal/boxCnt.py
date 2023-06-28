from concurrent.futures import ProcessPoolExecutor as Pool
from math import log10
from os import mkdir, system
from os.path import isdir

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.api import OLS, add_constant

from sphractal.surfExact import findTargetAtoms, MIN_VAL_FROM_BOUND, scanAllAtoms, writeBoxCoords
from sphractal.surfPointClouds import genSurfPoints
from sphractal.utils import estDuration, findNN, findSurf, readXYZ
# from sphractal.utils import annotate


NUM_BOX_LEN_SAMPLE = 10
MIN_SAMPLE_NUM = 5
CONF_INT_PERC = 95  # Percentage
ALPHA_CI = 1 - CONF_INT_PERC/100


# @annotate('getVoxelBoxCnts', color='blue')
def getVoxelBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                    npName, writeFileDir='boxCntOutputs', exeDir='../bin', procUnit='cpu',
                    radType='metallic', numPoint=300, gridNum=1024,
                    rmInSurf=True, vis=True, verbose=True, genPCD=False):
    """
    Count the boxes that cover the outer surface of a set of overlapping spheres represented as point clouds for
    different box sizes, using 3D box-counting algorithm written by Ruiz de Miras et al. in C++. All source codes are
    provided under {SPHRACTAL_DIR_PATH}/src/fbc/.
    
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
    writeFileDir : str
        Path to the directory to store the output files.
    exeDir : str
        Path to the compiled C++ executable for box-counting.
    procUnit : {'cpu', 'gpu'}
        Type of C++ executable to run for box-counting.
    radType : {'metallic', 'atomic'}
        Type of radii to use for the spheres.
    numPoint : int 
        Number of surface points to be generated around each atom.
    gridNum : int
        Resolution of the 3D binary image.
    rmInSurf : bool
        Whether to remove the surface points on the inner surface.
    vis : bool 
        Whether to generate output files for visualisation.
    verbose : bool
        Whether to display the details.
    genPCD : bool
        Whether to generate pcd file for box-counting using MATLAB code written by Kazuaki Iida.
    
    Returns
    -------
    scaleChange : list
        Box lengths.
    cntChange : list
        Number of boxes that cover the surface of interest, as represented by the voxels in the 3D binary image.

    Examples
    --------
    >>> eles, rads, xyzs, _, minxyz, maxxyz = readXYZ('example.xyz')
    >>> neighs, _ = findNN(rads, xyzs, minxyz, maxxyz, 2.5)
    >>> surfs = findSurf(xyzs, neighs, 'alphaShape', 5.0)
    >>> scales, counts = genSurfPoints(eles, rads, surfs, xyzs, neighs, 'example')

    Notes
    -----
    The 3D binary image resolution (gridNum) is restricted by RAM size available, the relationship is illustrated below:
    -  1024 ->    2 GB (laptops -> typically 8 GB)
    -  2048 ->   16 GB (HPC nodes with GPUs like NCI Gadi gpuvolta queue -> max 32 GB/node)
    -  4096 ->  128 GB
    -  8192 -> 1024 GB (HPC node with huge memories like NCI Gadi megamem queue -> max 2990 GB/node)
    - 16384 -> 8192 GB
    Further details about maximum grid size and memory estimation could be found in original codes of the authors in
    {SPHRACTAL_DIR_PATH}/src/fbc/test.cpp.
    As a reference, when 8192 grids are used, allocation of memory took 25 min; while the CPU algorithm runs for 18 min.
    """
    if verbose:
        print(f"  Approximating the surface with {numPoint} point clouds for each atom...")

    genSurfPoints(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                  npName, writeFileDir,
                  radType, numPoint, gridNum,
                  rmInSurf, vis, verbose, genPCD)
    system(f"{exeDir}/3DbinImBC{procUnit}.exe {gridNum} {writeFileDir}/surfVoxelIdxs.txt "
           f"{writeFileDir}/surfVoxelBoxCnts.txt")
    scaleChange, cntChange = [], []
    with open(f"{writeFileDir}/surfVoxelBoxCnts.txt", 'r') as f:
        for line in f:
            scaleChange.append(log10(1 / int(line.split()[0])))
            cntChange.append(log10(int(line.split()[1])))
    return scaleChange[::-1], cntChange[::-1]


# @annotate('getSphereBoxCnts', color='blue')
def getSphereBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                     maxDimDiff, minMaxBoxLens, minXYZ, npName, writeFileDir='boxCntOutputs',
                     rmInSurf=True, writeBox=True, verbose=True, boxLenConc=False, maxWorkers=2):
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
    maxDimDiff : float
        Maximum range among all dimensions of the Cartesian space, defines the borders of the largest box.
    minMaxBoxLens : tuple of floats
        Minimum and maximum box lengths.
    minXYZ : 1D ndarray
        Minimum values of each dimension in the Cartesian space.
    npName : str
        Identifier of the measured object, which forms part of the output file name, ideally unique.
    writeFileDir : str
        Path to the directory to store the output files.
    rmInSurf : bool 
        Whether to remove the surface points on the inner surface.
    writeBox : bool
        Whether to generate output files for visualisation.
    verbose : bool
        Whether to display the details.
    boxLenConc : bool
        Whether to parallelise the box-counting across different box lengths.
    maxWorkers : int
        Maximum number of processes to spawn for parallelisation of box-counting across different box lengths, only used
        if 'boxLenConc' is True.
    
    Returns
    -------
    scaleChange : list
        Box lengths.
    cntChange : list
        Number of boxes that cover the exact spherical surface of interest.
    
    Examples
    --------
    >>> eles, rads, xyzs, _, minxyz, maxxyz = readXYZ('example.xyz')
    >>> neighs, _ = findNN(rads, xyzs, minxyz, maxxyz, 2.5)
    >>> surfs = findSurf(xyzs, neighs, 'alphaShape', 5.0)
    >>> scales, counts = getSphereBoxCnts(eles, rads, surfs, xyzs, neighs, 100, (0.2, 1), minxyz, 'example')
    """
    if verbose:
        print(f"  Representing the surface by treating each atom as exact spheres...")
        print(f"    (1/r)    (# bulk)    (# surf)")
    atomsIdxs = atomsSurfIdxs if rmInSurf else findTargetAtoms(atomsNeighIdxs)
    overallBoxLen = maxDimDiff + MIN_VAL_FROM_BOUND * 2
    allLensSurfBoxs, allLensBulkBoxs, allLensSurfCnts, allLensBulkCnts = [], [], [], []
    scaleChange, scanBoxLens, scanAllAtomsInps = [], [], []
    approxScanBoxLens = np.geomspace(minMaxBoxLens[1], minMaxBoxLens[0], num=NUM_BOX_LEN_SAMPLE)
    for approxScanBoxLen in approxScanBoxLens:  # Evenly reduced box lengths on log scale
        magnFac = int(overallBoxLen / approxScanBoxLen)
        scanBoxLen = overallBoxLen / magnFac
        scanAllAtomsInp = (magnFac, scanBoxLen, atomsIdxs, minXYZ,
                           atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs, 
                           rmInSurf, verbose)
        if boxLenConc:
            scanAllAtomsInps.append(scanAllAtomsInp) 
        else:
            scanAllAtomsResult = scanAllAtoms(scanAllAtomsInp) 
            allAtomsSurfBoxs, allAtomsBulkBoxs = scanAllAtomsResult
            allLensSurfBoxs.append(allAtomsSurfBoxs)
            allLensBulkBoxs.append(allAtomsBulkBoxs)
            allLensSurfCnts.append(len(allAtomsSurfBoxs))

        scaleChange.append(log10(magnFac / overallBoxLen))
        scanBoxLens.append(scanBoxLen)

    if boxLenConc:
        with Pool(max_workers=maxWorkers) as pool:
            for scanAllAtomsResult in pool.map(scanAllAtoms, scanAllAtomsInps):
                allAtomsSurfBoxs, allAtomsBulkBoxs = scanAllAtomsResult
                allLensSurfBoxs.append(allAtomsSurfBoxs)
                allLensBulkBoxs.append(allAtomsBulkBoxs)
                allLensSurfCnts.append(len(allAtomsSurfBoxs))
    cntChange = [log10(sCnt) if sCnt != 0 else np.nan for sCnt in allLensSurfCnts]

    if writeBox:
        writeBoxCoords(atomsEle, atomsXYZ, allLensSurfBoxs, allLensBulkBoxs, minXYZ, scanBoxLens, writeFileDir, npName)
    return scaleChange, cntChange


# @annotate('findSlope', color='green')
def findSlope(scaleChange, cntChange, writeFileDir, npName='', lenRange='trim',
              visReg=False, saveFig=False, showPlot=False):
    """Compute the slope (box counting dimension) from the box-counting data collected."""
    while np.nan in cntChange:
        nanIdx = cntChange.index(np.nan)
        del cntChange[nanIdx]
        del scaleChange[nanIdx]
    firstPointIdx, lastPointIdx, removeSmallBoxes = 0, len(scaleChange), True  # countChange.count(countChange[0])
    r2score, boxCntDim, slopeCI, r2scorePrev, boxCntDimPrev, slopeCIPrev = 0.0, 0.0, (0.0, 0.0), 0.0, 0.0, (0.0, 0.0)
    while len(scaleChange[firstPointIdx:lastPointIdx]) > MIN_SAMPLE_NUM:
        x, y = scaleChange[firstPointIdx:lastPointIdx], cntChange[firstPointIdx:lastPointIdx]
        regModel = OLS(endog=y, exog=add_constant(x)).fit()
        r2score, boxCntDim, slopeCI = regModel.rsquared, regModel.params[1], regModel.conf_int(alpha=ALPHA_CI)[1]
        yPred = regModel.predict()  # Returns ndarray, allowing subtraction later
        if visReg:
            plt.clf()
            plt.scatter(x, y)
            plt.plot(x, yPred, label='OLS')
            predOLS = regModel.get_prediction()
            lowCIvals, upCIvals = predOLS.summary_frame()['mean_ci_lower'], predOLS.summary_frame()['mean_ci_upper']
            plt.plot(x, upCIvals, 'r--')
            plt.plot(x, lowCIvals, 'r--')
            plt.xlabel('log(1/r)')
            plt.ylabel('log(N)')
            plt.title(f"{npName} R2: {r2score:.3f}, D_Box: {boxCntDim:.3f}, {CONF_INT_PERC}% CI: "
                      f"[{slopeCI[0]:.3f}, {slopeCI[1]:.3f}]")
        # Removal of next point (beware of weird behaviour in middle range)
        # lstSqErrs = np.subtract(y, yPred) ** 2
        # if len(y) % 2 == 0:
        #     lowBoundErrSum, upBoundErrSum = lstSqErrs[:len(y) // 2].sum(), lstSqErrs[len(y) // 2:].sum()
        # else:
        #     lowBoundErrSum, upBoundErrSum = lstSqErrs[:len(y) // 2].sum(), lstSqErrs[len(y) // 2 + 1:].sum()
        # if lowBoundErrSum > upBoundErrSum: firstPointIdx += 1
        # else: lastPointIdx -= 1
        if lenRange == 'trim':
            if removeSmallBoxes:
                if round(r2score, 3) < round(r2scorePrev, 3):
                    removeSmallBoxes = False
                lastPointIdx -= 1
            else:
                if round(r2score, 3) < round(r2scorePrev, 3):
                    return r2scorePrev, boxCntDimPrev, slopeCIPrev
                firstPointIdx += 1
        if saveFig:
            boxCntDimsDir = f"{writeFileDir}/boxCntDims"
            if not isdir(boxCntDimsDir):
                mkdir(boxCntDimsDir)
            plt.savefig(f"{boxCntDimsDir}/{npName}_boxCntDim.png")
        if showPlot:
            plt.show()
        r2scorePrev, boxCntDimPrev, slopeCIPrev = r2score, boxCntDim, slopeCI
        if lenRange == 'full':
            return r2score, boxCntDim, slopeCI
    return r2score, boxCntDim, slopeCI


# @annotate('runCase', color='cyan')
@estDuration
def runBoxCnt(xyzFilePath, 
              radType='metallic', calcBL=False, findSurfOption='alphaShape', alphaMult=2.5,
              writeFileDir='boxCntOutputs', lenRange='trim', 
              rmInSurf=True, vis=True, saveFig=True, showPlot=False, verbose=True,
              runPointCloudBoxCnt=True, numPoints=300, gridNum=1024, exeDir='../bin', procUnit='cpu', genPCD=False,
              runExactSphereBoxCnt=True, minLenMult=0.25, maxLenMult=1, writeBox=True, boxLenConc=False, maxWorkers=2):
    """
    Run box-counting algorithm on the surface of a given object consisting of a set of spheres represented as either
    point clouds or exact spherical surface.
    
    Parameters
    ----------
    xyzFilePath : str
        Path to an xyz file containing the Cartesian coordinates of a set of spheres.
    radType : {'metallic', 'atomic'}
        Type of radii to use for the spheres.
    calcBL : bool
        Whether to compute the average distance from its neighbours for each atom
    findSurfOption : {'alphaShape', 'convexHull', 'numNeigh'}
        Algorithm to identify the spheres on the surface.
    alphaMult : float 
        Multiplier to the minimum spherical radii to decide 'alpha' for the alpha shape algorithm, only used if
        'findSurfOption' is 'alphaShape'.
    writeFileDir : str
        Path to the directory to store the output files.
    lenRange : {'trim', 'full'} 
        Range of box lengths to include for determining the box-counting dimension. Choosing 'trim' finds the highest 
        coefficient of determination by iteratively removing the box counts obtained using boxes of extreme sizes.
    rmInSurf : bool
        Whether to remove the surface points on the inner surface.
    vis : bool 
        Whether to generate output files for visualisation.
    saveFig : bool
        Whether to save the plots generated, only used if 'vis' is True.
    showPlot : bool
        Whether to show the plots generated, only used if 'vis' is True.
    verbose : bool
        Whether to display the details.
    runPointCloudBoxCnt : bool
        Whether to represent the surface as point clouds.
    numPoints : int
        Number of surface points to be generated around each atom.
    gridNum : int
        Resolution of the 3D binary image.
    exeDir : str
        Path to the compiled C++ executable for box-counting.
    procUnit : {'cpu', 'gpu'}
        Type of C++ executable to run for box-counting.
    genPCD : bool
        Whether to generate pcd file for box-counting using MATLAB code written by Kazuaki Iida.
    runExactSphereBoxCnt : bool
        Whether to represent the surface as exact spheres.
    minLenMult : float
        Multiplier to the minimum radii to determine the minimum box length for box-counting dimension estimation.
    maxLenMult : float
        Multiplier to the minimum radii to determine the maximum box length for box-counting dimension estimation.
    writeBox : bool
        Whether to generate output files for visualisation.
    boxLenConc : bool
        Whether to parallelise the box-counting across different box lengths.
    maxWorkers : int
        Maximum number of processes to spawn for parallelisation of box-counting across different box sizes, only used
        if 'boxLenConc' is True.
    
    Returns
    -------
    r2PC : float
        Coefficient of determination from determination of the dimension of point clouds surface.
    bcDimPC : float
        Box-counting dimension of the point clouds representation of the surface.
    confIntPC : tuple
        Confidence interval of the box-counting dimension of the point clouds surface.
    r2ES : float
        Coefficient of determination from determination of the dimension of exact sphere surface.
    bcDimES : float
        Box-counting dimension of the exact sphere representation of the surface.
    confIntES : tuple
        Confidence interval of the box-counting dimension of the exact sphere surface.
    
    Examples
    --------
    >>> r2Points, bcDimPoints, confIntPoints, r2Exact, bcDimExact, confIntExact = runBoxCnt('example.xyz')
    """
    radMult = 1.5 if radType == 'metallic' else 1.2  # Radius multiplier to identify nearest neighbour
    atomsEle, atomsRad, atomsXYZ, maxDimDiff, minXYZ, maxXYZ = readXYZ(xyzFilePath, radType)
    atomsNeighIdxs, atomsAvgBondLen = findNN(atomsRad, atomsXYZ, minXYZ, maxXYZ, atomsRad.max(), radMult, calcBL)
    atomsSurfIdxs = findSurf(atomsXYZ, atomsNeighIdxs, findSurfOption, alphaMult * atomsRad.min())
    testCase = xyzFilePath.split('/')[-1][:-4]
    if verbose:
        print(f"\n{testCase}")

    r2PC, bcDimPC, confIntPC = np.nan, np.nan, (np.nan, np.nan)
    r2ES, bcDimES, confIntES = np.nan, np.nan, (np.nan, np.nan)
    if not isdir(writeFileDir):
        mkdir(writeFileDir)
    if runPointCloudBoxCnt:
        scalesPC, countsPC = getVoxelBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                             testCase, writeFileDir, exeDir, procUnit,
                                             radType, numPoints, gridNum,
                                             rmInSurf, vis, verbose, genPCD)
        r2PC, bcDimPC, confIntPC = findSlope(scalesPC, countsPC, writeFileDir, testCase, lenRange,
                                             vis, saveFig, showPlot)
    if runExactSphereBoxCnt:
        minAtomRad = atomsRad.min()
        scalesES, countsES = getSphereBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                              maxDimDiff, (minAtomRad * minLenMult, minAtomRad * maxLenMult),
                                              minXYZ, testCase, writeFileDir,
                                              rmInSurf, writeBox, verbose, boxLenConc, maxWorkers)
        r2ES, bcDimES, confIntES = findSlope(scalesES, countsES, writeFileDir, testCase, lenRange,
                                             vis, saveFig, showPlot)
    if verbose:
        if runPointCloudBoxCnt:
            print(f"  Point clouds  D_Box: {bcDimPC:.4f} [{confIntPC[0]:.4f}, {confIntPC[1]:.4f}],  R2: {r2PC:.4f}")
        if runExactSphereBoxCnt:
            print(f"  Exact surface D_Box: {bcDimES:.4f} [{confIntES[0]:.4f}, {confIntES[1]:.4f}],  R2: {r2ES:.4f}")
    return r2PC, bcDimPC, confIntPC, r2ES, bcDimES, confIntES
