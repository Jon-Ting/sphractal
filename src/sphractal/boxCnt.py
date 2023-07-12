from os import mkdir
from os.path import isdir
from warnings import warn

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from statsmodels.api import OLS, add_constant

from sphractal.constants import PLT_PARAMS
from sphractal.utils import findNN, findSurf, readInp
from sphractal.surfVoxel import voxelBoxCnts
from sphractal.surfExact import exactBoxCnts
# from sphractal.utils import estDuration, annotate


# @annotate('findSlope', color='green')
def findSlope(scales, counts, npName='', outDir='boxCntOutputs', lenRange='trim',
              minSample=5, confLvl=95, 
              visReg=True, figType='paper', saveFig=False, showPlot=False):
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
    outDir : str, optional
        Path to the directory to store the output files.
    lenRange : {'trim', 'full'}, optional
        Range of box lengths to include for determining the box-counting dimension. Choosing 'trim' finds the highest 
        coefficient of determination by iteratively removing the box counts obtained using boxes of extreme sizes.
    minSample : int, optional
        Minimum number of box count data points to be retained for slope estimation from the linear regression fitting.
    confLvl : Union[int, float]
        Confidence level of confidence interval in percentage.
    visReg : bool, optional
        Whether to generate figures from the linear regression fitting process.
    figType : {'paper', 'poster', 'talk'}
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
        figSize, dpi, fontSize, labelSize = params['figSize'], params['dpi'], params['fontSize'], params['labelSize']
        legendSize, lineWidth, markerSize = params['legendSize'], params['lineWidth'], params['markerSize']
    else:
        figSize = dpi = fontSize = labelSize = legendSize = lineWidth = markerSize = None

    # Remove invalid entries in the box counts data collected
    while np.nan in counts:
        nanIdx = counts.index(np.nan)
        del counts[nanIdx]
        del scales[nanIdx]

    if abs(confLvl) > 100:
        warn(f"Confidence level out of range, confidence intervals are unreliable! 'confLvl' should be within [0, 100) "
             f"instead of {confLvl}")
    alphaCI = 1 - confLvl/100

    firstPointIdx, lastPointIdx, removeSmallBoxes = 0, len(scales), True
    r2score, boxCntDim, slopeCI = 0.0, 0.0, np.array((np.inf, np.inf))
    r2scorePrev, boxCntDimPrev, slopeCIPrev = 0.0, 0.0, np.array((np.inf, np.inf))
    while len(scales[firstPointIdx:lastPointIdx]) > minSample:

        x, y = scales[firstPointIdx:lastPointIdx], counts[firstPointIdx:lastPointIdx]
        regModel = OLS(endog=y, exog=add_constant(x)).fit()
        r2score, boxCntDim, slopeCI = regModel.rsquared, regModel.params[1], regModel.conf_int(alpha=alphaCI)[1]
        yPred = regModel.predict()  # Returns ndarray, allowing subtraction later

        if visReg:
            plt.close()
            fig = plt.figure(figsize=figSize, dpi=dpi)
            ax = fig.add_subplot(1, 1, 1)
            handleScatter = ax.scatter(x, y, marker='o', s=markerSize, c='r', alpha=1, edgecolors='k', linewidths=1.2,
                                       zorder=3)
            handleBestFit = ax.plot(x, yPred, linestyle='-', linewidth=1., color='k', label='OLS')
            ax.grid(linestyle='dotted')

            # Compute confidence bands
            predOLS = regModel.get_prediction()
            lowCIs, upCIs = predOLS.summary_frame()['mean_ci_lower'], predOLS.summary_frame()['mean_ci_upper']
            handleConfBand = ax.plot(x, upCIs, linestyle='--', linewidth=lineWidth, color='b')
            ax.plot(x, lowCIs, linestyle='--', linewidth=lineWidth, color='b')
            ax.fill_between(x, upCIs, lowCIs, alpha=0.2)

            ax.set_xlabel(r'log$(1/\epsilon)$', fontsize=labelSize)
            ax.set_ylabel(r'log$(N)$', fontsize=labelSize)
            ax.yaxis.set_major_formatter(FormatStrFormatter('% 1.1f'))
            # ax.set_title('', fontsize=fontSize)
            ax.legend(handles=(handleScatter, handleBestFit[0], handleConfBand[0]), 
                      labels=('Actual box counts', fr"Best fit line ($R^2$: {r2score:.3f})",
                              f"{confLvl}% confidence bands"),
                      title=fr"$D_{{box}}$: {boxCntDim:.3f} [{slopeCI[0]:.3f}, {slopeCI[1]:.3f}]",
                      title_fontsize=legendSize,
                      fontsize=legendSize)
            plt.tight_layout()

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
        r2scorePrev, boxCntDimPrev, slopeCIPrev = r2score, boxCntDim, slopeCI

        if saveFig:
            boxCntDimsDir = f"{outDir}/boxCntDims"
            if not isdir(boxCntDimsDir):
                if not isdir(outDir):
                    mkdir(outDir)
                mkdir(boxCntDimsDir)
            plt.savefig(f"{boxCntDimsDir}/{npName}_boxCntDim.png", bbox_inches='tight')
        if showPlot:
            plt.show()
        if lenRange == 'full':
            break
    return r2score, boxCntDim, slopeCI


# @annotate('runCase', color='cyan')
# @estDuration
def runBoxCnt(inpFilePath, 
              radType='atomic', calcBL=False, findSurfAlg='alphaShape', alphaMult=2.0,
              outDir='boxCntOutputs', lenRange='trim', minSample=5, confLvl=95, 
              rmInSurf=True, vis=True, figType='paper', saveFig=False, showPlot=False, verbose=False,
              voxelSurf=True, numPoints=300, gridNum=1024, exePath='$FASTBC_EXE', genPCD=False,
              exactSurf=True, minLenMult=0.25, maxLenMult=1, numBoxLen=10, bufferDist=5.0, writeBox=True): 
    """
    Run box-counting algorithm on the surface of a given object consisting of a set of spheres represented as either
    point clouds or exact spherical surface.
    
    Parameters
    ----------
    inpFilePath : str
        Path to an xyz file containing the Cartesian coordinates of a set of spheres.
    radType : {'atomic', 'metallic'}, optional
        Type of radii to use for the spheres.
    calcBL : bool, optional
        Whether to compute the average distance from its neighbours for each atom
    findSurfAlg : {'alphaShape', 'convexHull', 'numNeigh'}, optional
        Algorithm to identify the spheres on the surface.
    alphaMult : Union[int, float], optional
        Multiplier to the minimum spherical radii to decide 'alpha' for the alpha shape algorithm, only used if
        'findSurfAlg' is 'alphaShape'.
    outDir : str, optional
        Path to the directory to store the output files.
    lenRange : {'trim', 'full'}, optional
        Range of box lengths to include for determining the box-counting dimension. Choosing 'trim' finds the highest 
        coefficient of determination by iteratively removing the box counts obtained using boxes of extreme sizes.
    minSample : int, optional
        Minimum number of box count data points to be retained for slope estimation from the linear regression fitting.
    confLvl : Union[int, float], optional
        Confidence level of confidence interval in percentage.
    rmInSurf : bool, optional
        Whether to remove the surface points on the inner surface.
    vis : bool, optional
        Whether to generate output files for visualisation.
    figType : {'paper', 'poster', 'talk'}
        Type of figures to be generated.
    saveFig : bool, optional
        Whether to save the plots generated, only used if 'vis' is True.
    showPlot : bool, optional
        Whether to show the plots generated, only used if 'vis' is True.
    verbose : bool, optional
        Whether to display the details.
    voxelSurf : bool, optional
        Whether to represent the surface as point clouds.
    numPoints : int, optional
        Number of surface points to be generated around each atom.
    gridNum : int, optional
        Resolution of the 3D binary image.
    exePath : str, optional
        Path to the compiled C++ executable for box-counting.
    genPCD : bool, optional
        Whether to generate pcd file for box-counting using MATLAB code written by Kazuaki Iida.
    exactSurf : bool, optional
        Whether to represent the surface as exact spheres.
    minLenMult : float, optional
        Multiplier to the minimum radii to determine the minimum box length for box-counting dimension estimation.
    maxLenMult : float, optional
        Multiplier to the minimum radii to determine the maximum box length for box-counting dimension estimation.
    numBoxLen : int, optional
        Number of box lengths to use for the collection of the box count data, spaced evenly on logarithmic scale.
    bufferDist : Union[int,float]
        Buffer distance from the borders of the largest box in Angstrom.
    writeBox : bool, optional
        Whether to generate output files for visualisation.
    
    Returns
    -------
    r2VX : float
        Coefficient of determination from determination of the dimension of point clouds surface.
    bcDimVX : float
        Box-counting dimension of the point clouds representation of the surface.
    confIntVX : tuple
        Confidence interval of the box-counting dimension of the point clouds surface.
    r2EX : float
        Coefficient of determination from determination of the dimension of exact sphere surface.
    bcDimEX : float
        Box-counting dimension of the exact sphere representation of the surface.
    confIntEX : tuple
        Confidence interval of the box-counting dimension of the exact sphere surface.
    
    Examples
    --------
    >>> r2Points, bcDimPoints, confIntPoints, r2Exact, bcDimExact, confIntExact = runBoxCnt('example.xyz')
    """
    radMult = 1.2 if radType == 'atomic' else 1.5  # Radius multiplier to identify nearest neighbour
    atomsEle, atomsRad, atomsXYZ, maxRange, minXYZ, maxXYZ = readInp(inpFilePath, radType)
    atomsNeighIdxs, atomsAvgBondLen = findNN(atomsRad, atomsXYZ, minXYZ, maxXYZ, atomsRad.max(), radMult, calcBL)
    atomsSurfIdxs = findSurf(atomsXYZ, atomsNeighIdxs, findSurfAlg, alphaMult * atomsRad.min())
    testCase = inpFilePath.split('/')[-1][:-4]
    if verbose:
        print(f"\n{testCase}")

    r2VX, bcDimVX, confIntVX = np.nan, np.nan, (np.nan, np.nan)
    r2EX, bcDimEX, confIntEX = np.nan, np.nan, (np.nan, np.nan)
    if not isdir(outDir):
        mkdir(outDir)
    if voxelSurf:
        scalesVX, countsVX = voxelBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                          testCase, outDir, exePath,
                                          radType, numPoints, gridNum,
                                          rmInSurf, vis, verbose, genPCD)
        r2VX, bcDimVX, confIntVX = findSlope(scalesVX, countsVX, f"{testCase}_VX", outDir, lenRange,
                                             minSample, confLvl, vis, figType, saveFig, showPlot)
    if exactSurf:
        minAtomRad = atomsRad.min()
        scalesEX, countsEX = exactBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                          maxRange, (minAtomRad * minLenMult, minAtomRad * maxLenMult),
                                          minXYZ, testCase, outDir, numBoxLen, bufferDist,
                                          rmInSurf, writeBox, verbose)
        r2EX, bcDimEX, confIntEX = findSlope(scalesEX, countsEX, f"{testCase}_EX", outDir, lenRange,
                                             minSample, confLvl, vis, figType, saveFig, showPlot)
    if verbose:
        if voxelSurf:
            print(f"  Point clouds  D_Box: {bcDimVX:.4f} [{confIntVX[0]:.4f}, {confIntVX[1]:.4f}],  R2: {r2VX:.4f}")
        if exactSurf:
            print(f"  Exact surface D_Box: {bcDimEX:.4f} [{confIntEX[0]:.4f}, {confIntEX[1]:.4f}],  R2: {r2EX:.4f}")
    return r2VX, bcDimVX, confIntVX, r2EX, bcDimEX, confIntEX
