from concurrent.futures import ProcessPoolExecutor as Pool
from math import log10
from os import mkdir, system
from os.path import isdir
from warnings import warn

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from statsmodels.api import OLS, add_constant

from sphractal.constants import PLT_PARAMS
from sphractal.utils import findNN, findSurf, readXYZ
# from sphractal.utils import estDuration, annotate
from sphractal.surfPointClouds import genSurfPoints
from sphractal.surfExact import findTargetAtoms, MIN_VAL_FROM_BOUND, scanAllAtoms, writeBoxCoords


# @annotate('getVoxelBoxCnts', color='blue')
def getVoxelBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                    npName, writeFileDir='boxCntOutputs', exePath='$FASTBC_EXE',
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
    writeFileDir : str, optional
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
    Further details about maximum grid size and memory estimation could be found in 'test.cpp' documented by the authors 
    (https://www.ugr.es/~demiras/fbc/). As a reference, when 8192 grids are used, allocation of memory took 25 min; while 
    the CPU algorithm runs for 18 min.
    """
    if verbose:
        print(f"  Approximating the surface with {numPoint} point clouds for each atom...")
    if not isdir(writeFileDir):
        mkdir(writeFileDir)

    genSurfPoints(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                  npName, writeFileDir,
                  radType, numPoint, gridNum,
                  rmInSurf, vis, verbose, genPCD)
    system(f"{exePath} {gridNum} {writeFileDir}/surfVoxelIdxs.txt {writeFileDir}/surfVoxelBoxCnts.txt")
    scales, counts = [], []
    with open(f"{writeFileDir}/surfVoxelBoxCnts.txt", 'r') as f:
        for line in f:
            scales.append(log10(1 / int(line.split()[0])))
            counts.append(log10(int(line.split()[1])))
    return scales[::-1], counts[::-1]


# @annotate('getSphereBoxCnts', color='blue')
def getSphereBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                     maxRange, minMaxBoxLens, minXYZ, npName, writeFileDir='boxCntOutputs', numBoxLenSample=10,
                     rmInSurf=True, writeBox=True, verbose=False, boxLenConc=False, maxWorkers=2):
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
    writeFileDir : str, optional
        Path to the directory to store the output files.
    numBoxLenSample : int, optional
        Number of box lengths to use for the collection of the box count data, spaced evenly on logarithmic scale.
    rmInSurf : bool, optional
        Whether to remove the surface points on the inner surface.
    writeBox : bool, optional
        Whether to generate output files for visualisation.
    verbose : bool, optional
        Whether to display the details.
    boxLenConc : bool, optional
        Whether to parallelise the box-counting across different box lengths (under development, stick to default for now).
    maxWorkers : int, optional
        Maximum number of processes to spawn for parallelisation of box-counting across different box lengths, only used
        if 'boxLenConc' is True.
    
    Returns
    -------
    scales : list
        Box lengths.
    counts : list
        Number of boxes that cover the exact spherical surface of interest.
    
    Examples
    --------
    >>> eles, rads, xyzs, _, minxyz, maxxyz = readXYZ('example.xyz')
    >>> neighs, _ = findNN(rads, xyzs, minxyz, maxxyz, 1.2)
    >>> surfs = findSurf(xyzs, neighs, 'alphaShape', 2.0)
    >>> scales, counts = getSphereBoxCnts(eles, rads, surfs, xyzs, neighs, 100, (0.2, 1), minxyz, 'example')
    """
    if verbose:
        print(f"  Representing the surface by treating each atom as exact spheres...")
        print(f"    (1/eps)    (# bulk)    (# surf)")
    if writeBox:
        if not isdir(writeFileDir):
            mkdir(writeFileDir)

    atomsIdxs = atomsSurfIdxs if rmInSurf else findTargetAtoms(atomsNeighIdxs)
    overallBoxLen = maxRange + MIN_VAL_FROM_BOUND * 2
    allLensSurfBoxs, allLensBulkBoxs, allLensSurfCnts, allLensBulkCnts = [], [], [], []
    scales, scanBoxLens, scanAllAtomsInps = [], [], []
    approxScanBoxLens = np.geomspace(minMaxBoxLens[1], minMaxBoxLens[0], num=numBoxLenSample)
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

        scales.append(log10(magnFac / overallBoxLen))
        scanBoxLens.append(scanBoxLen)

    if boxLenConc:
        with Pool(max_workers=maxWorkers) as pool:
            for scanAllAtomsResult in pool.map(scanAllAtoms, scanAllAtomsInps):
                allAtomsSurfBoxs, allAtomsBulkBoxs = scanAllAtomsResult
                allLensSurfBoxs.append(allAtomsSurfBoxs)
                allLensBulkBoxs.append(allAtomsBulkBoxs)
                allLensSurfCnts.append(len(allAtomsSurfBoxs))
    counts = [log10(sCnt) if sCnt != 0 else np.nan for sCnt in allLensSurfCnts]

    if writeBox:
        writeBoxCoords(atomsEle, atomsXYZ, allLensSurfBoxs, allLensBulkBoxs, minXYZ, scanBoxLens, writeFileDir, npName)
    return scales, counts


# @annotate('findSlope', color='green')
def findSlope(scales, counts, npName='', writeFileDir='boxCntOutputs', lenRange='trim',
              minSampleNum=5, confLvl=95, 
              visReg=True, figType='article', saveFig=False, showPlot=False):
    """
    Compute the slope (box counting dimension) from the box-counting data collected.

    Parameters
    ----------
    scales : list
        Box lengths.
    counts : list
        Number of boxes that cover the exact spherical surface of interest.
    npName : str, optional
        Identifier of the measured object, which forms part of the output file name, ideally unique.
    writeFileDir : str, optional
        Path to the directory to store the output files.
    lenRange : {'trim', 'full'}, optional
        Range of box lengths to include for determining the box-counting dimension. Choosing 'trim' finds the highest 
        coefficient of determination by iteratively removing the box counts obtained using boxes of extreme sizes.
    minSampleNum : int, optional
        Minimum number of box count data points to be retained for slope estimation from the linear regression fitting.
    confLvl : Union[int, float]
        Confidence level of confidence interval in percentage.
    visReg : bool, optional
        Whether to generate figures from the linear regression fitting process.
    figType : {'article', 'poster', 'ppt'}
        Type of figures to be generated.
    saveFig : bool, optional
        Whether to save the plots generated, only works when 'visReg' is True.
    showPlot : bool, optional
        Whether to show the plots generated, only works when 'visReg' is True.
    
    Returns
    -------
    r2score : float
        Coefficient of determination from determination of the dimension of point clouds surface.
    boxCntDim : float
        Box-counting dimension of the point clouds representation of the surface.
    slopeCI : tuple
        Confidence interval of the box-counting dimension of the point clouds surface.
    """
    if visReg:
        plt.rc('font', family='sans-serif')
        plt.rc('xtick', labelsize='x-small')
        plt.rc('ytick', labelsize='x-small')
        params = PLT_PARAMS[figType]
        figsize, dpi, fontsize, labelsize, legendsize, linewidth, markersize = params['figsize'], params['dpi'], params['fontsize'], params['labelsize'], params['legendsize'], params['linewidth'], params['markersize']

    while np.nan in counts:
        nanIdx = counts.index(np.nan)
        del counts[nanIdx]
        del scales[nanIdx]
    firstPointIdx, lastPointIdx, removeSmallBoxes = 0, len(scales), True  # countChange.count(countChange[0])

    if abs(confLvl) > 100:
        warn(f"Confidence level out of range, confidence intervals are unreliable! 'confLvl' should be within [0, 100) instead of {confLvl}")
    alphaCI = 1 - confLvl/100
    r2score, boxCntDim, slopeCI, r2scorePrev, boxCntDimPrev, slopeCIPrev = 0.0, 0.0, np.array((np.inf, np.inf)), 0.0, 0.0, np.array((np.inf, np.inf))
    while len(scales[firstPointIdx:lastPointIdx]) > minSampleNum:
        x, y = scales[firstPointIdx:lastPointIdx], counts[firstPointIdx:lastPointIdx]
        regModel = OLS(endog=y, exog=add_constant(x)).fit()
        r2score, boxCntDim, slopeCI = regModel.rsquared, regModel.params[1], regModel.conf_int(alpha=alphaCI)[1]
        yPred = regModel.predict()  # Returns ndarray, allowing subtraction later
        if visReg:
            plt.close()
            fig = plt.figure(figsize=figsize, dpi=dpi)
            ax = fig.add_subplot(1, 1, 1)
            handleScatter = ax.scatter(x, y, marker='o', s=markersize, c='r', alpha=1, edgecolors='k', linewidths=1.2, zorder=3)
            handleBestFit = ax.plot(x, yPred, linestyle='-', linewidth=1., color='k', label='OLS')
            ax.grid(linestyle='dotted')
            predOLS = regModel.get_prediction()
            lowCIvals, upCIvals = predOLS.summary_frame()['mean_ci_lower'], predOLS.summary_frame()['mean_ci_upper']
            handleConfBand = ax.plot(x, upCIvals, linestyle='--', linewidth=linewidth, color='b')
            ax.plot(x, lowCIvals, linestyle='--', linewidth=linewidth, color='b')
            ax.fill_between(x, upCIvals, lowCIvals, alpha=0.2)
            ax.set_xlabel(r'log$(1/\epsilon)$', fontsize=labelsize)
            ax.set_ylabel(r'log$(N)$', fontsize=labelsize)
            ax.yaxis.set_major_formatter(FormatStrFormatter('% 1.1f'))
            ax.legend(handles=(handleScatter, handleBestFit[0], handleConfBand[0]), 
                      labels=('Actual box counts', fr"Best fit line ($R^2$: {r2score:.3f})", f"{confLvl}% confidence bands"), 
                      title=fr"$D_{{box}}$: {boxCntDim:.3f} [{slopeCI[0]:.3f}, {slopeCI[1]:.3f}]", title_fontsize=legendsize, 
                      fontsize=legendsize)
            #plt.tight_layout()
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
                if not isdir(writeFileDir):
                    mkdir(writeFileDir)
                mkdir(boxCntDimsDir)
            plt.savefig(f"{boxCntDimsDir}/{npName}_boxCntDim.png", bbox_inches='tight')
        if showPlot:
            plt.show()
        r2scorePrev, boxCntDimPrev, slopeCIPrev = r2score, boxCntDim, slopeCI
        if lenRange == 'full':
            break
    return r2score, boxCntDim, slopeCI


# @annotate('runCase', color='cyan')
# @estDuration
def runBoxCnt(xyzFilePath, 
              radType='atomic', calcBL=False, findSurfOption='alphaShape', alphaMult=2.0,
              writeFileDir='boxCntOutputs', lenRange='trim', minSampleNum=5, confLvl=95, 
              rmInSurf=True, vis=True, figType='article', saveFig=False, showPlot=False, verbose=False,
              runPointCloudBoxCnt=True, numPoints=300, gridNum=1024, exePath='$FASTBC_EXE', genPCD=False,
              runExactSphereBoxCnt=True, minLenMult=0.25, maxLenMult=1, numBoxLenSample=10, writeBox=True, 
              boxLenConc=False, maxWorkers=2):
    """
    Run box-counting algorithm on the surface of a given object consisting of a set of spheres represented as either
    point clouds or exact spherical surface.
    
    Parameters
    ----------
    xyzFilePath : str
        Path to an xyz file containing the Cartesian coordinates of a set of spheres.
    radType : {'atomic', 'metallic'}, optional
        Type of radii to use for the spheres.
    calcBL : bool, optional
        Whether to compute the average distance from its neighbours for each atom
    findSurfOption : {'alphaShape', 'convexHull', 'numNeigh'}, optional
        Algorithm to identify the spheres on the surface.
    alphaMult : Union[int, float], optional
        Multiplier to the minimum spherical radii to decide 'alpha' for the alpha shape algorithm, only used if
        'findSurfOption' is 'alphaShape'.
    writeFileDir : str, optional
        Path to the directory to store the output files.
    lenRange : {'trim', 'full'}, optional
        Range of box lengths to include for determining the box-counting dimension. Choosing 'trim' finds the highest 
        coefficient of determination by iteratively removing the box counts obtained using boxes of extreme sizes.
    minSampleNum : int, optional
        Minimum number of box count data points to be retained for slope estimation from the linear regression fitting.
    confLvl : Union[int, float], optional
        Confidence level of confidence interval in percentage.
    rmInSurf : bool, optional
        Whether to remove the surface points on the inner surface.
    vis : bool, optional
        Whether to generate output files for visualisation.
    figType : {'article', 'poster', 'ppt'}
        Type of figures to be generated.
    saveFig : bool, optional
        Whether to save the plots generated, only used if 'vis' is True.
    showPlot : bool, optional
        Whether to show the plots generated, only used if 'vis' is True.
    verbose : bool, optional
        Whether to display the details.
    runPointCloudBoxCnt : bool, optional
        Whether to represent the surface as point clouds.
    numPoints : int, optional
        Number of surface points to be generated around each atom.
    gridNum : int, optional
        Resolution of the 3D binary image.
    exePath : str, optional
        Path to the compiled C++ executable for box-counting.
    genPCD : bool, optional
        Whether to generate pcd file for box-counting using MATLAB code written by Kazuaki Iida.
    runExactSphereBoxCnt : bool, optional
        Whether to represent the surface as exact spheres.
    minLenMult : float, optional
        Multiplier to the minimum radii to determine the minimum box length for box-counting dimension estimation.
    maxLenMult : float, optional
        Multiplier to the minimum radii to determine the maximum box length for box-counting dimension estimation.
    numBoxLenSample : int, optional
        Number of box lengths to use for the collection of the box count data, spaced evenly on logarithmic scale.
    writeBox : bool, optional
        Whether to generate output files for visualisation.
    boxLenConc : bool, optional
        Whether to parallelise the box-counting across different box lengths.
    maxWorkers : int, optional
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
    radMult = 1.2 if radType == 'atomic' else 1.5  # Radius multiplier to identify nearest neighbour
    atomsEle, atomsRad, atomsXYZ, maxRange, minXYZ, maxXYZ = readXYZ(xyzFilePath, radType)
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
                                             testCase, writeFileDir, exePath,
                                             radType, numPoints, gridNum,
                                             rmInSurf, vis, verbose, genPCD)
        r2PC, bcDimPC, confIntPC = findSlope(scalesPC, countsPC, f"{testCase}_PC", writeFileDir, lenRange,
                                             minSampleNum, confLvl, vis, figType, saveFig, showPlot)
    if runExactSphereBoxCnt:
        minAtomRad = atomsRad.min()
        scalesES, countsES = getSphereBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                              maxRange, (minAtomRad * minLenMult, minAtomRad * maxLenMult),
                                              minXYZ, testCase, writeFileDir, numBoxLenSample,
                                              rmInSurf, writeBox, verbose, boxLenConc, maxWorkers)
        r2ES, bcDimES, confIntES = findSlope(scalesES, countsES, f"{testCase}_ES", writeFileDir, lenRange,
                                             minSampleNum, confLvl, vis, figType, saveFig, showPlot)
    if verbose:
        if runPointCloudBoxCnt:
            print(f"  Point clouds  D_Box: {bcDimPC:.4f} [{confIntPC[0]:.4f}, {confIntPC[1]:.4f}],  R2: {r2PC:.4f}")
        if runExactSphereBoxCnt:
            print(f"  Exact surface D_Box: {bcDimES:.4f} [{confIntES[0]:.4f}, {confIntES[1]:.4f}],  R2: {r2ES:.4f}")
    return r2PC, bcDimPC, confIntPC, r2ES, bcDimES, confIntES
