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
def findSlope(scales, counts, npName='', outDir='outputs', trimLen=True,
              minSample=6, confLvl=95, 
              visReg=True, figType='paper', saveFig=False, showPlot=False, verbose=False):
    """
    Compute the slope (box counting dimension) from the box-counting data collected.

    Parameters
    ----------
    scales : list of floats
        Box lengths.
    counts : list of floats
        Number of boxes that cover the exact spherical surface of interest.
    npName : str, optional
        Identifier of the measured object, which forms part of the output file name, ideally unique.
    outDir : str, optional
        Path to the directory to store the output files.
    trimLen : bool, optional
        Whether to remove the box counts obtained using boxes of extreme sizes.
    minSample : int, optional
        Minimum number of box count data points to be retained for slope estimation from the linear regression fitting.
    confLvl : Union[int, float]
        Confidence level of confidence interval in percentage.
    visReg : bool, optional
        Whether to generate figures from the linear regression fitting process.
    figType : {'paper', 'poster', 'talk'}
        Type of figures to be generated.
    saveFig : bool, optional
        Whether to save the final figure generated, only works when 'visReg' is True.
    showPlot : bool, optional
        Whether to show the figures generated, only works when 'visReg' is True.
    verbose : bool, optional
        Whether to display the details.
    
    Returns
    -------
    r2score : float
        Coefficient of determination from determination of the dimension of point clouds surface.
    boxCntDim : float
        Box-counting dimension of the point clouds representation of the surface.
    slopeCI : 1D ndarray of floats
        Confidence interval of the box-counting dimension of the point clouds surface.
    minMaxLens : tuple of floats
        Minimum and maximum box lengths used to determine slope.
    """
    assert isinstance(minSample, int), 'minSample should be integer!'

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
    r2score, boxCntDim, slopeCI, minMaxLens = 0.0, 0.0, np.array((np.inf, np.inf)), (scales[0], scales[-1])
    r2scorePrev, boxCntDimPrev, slopeCIPrev, minMaxLensPrev = 0.0, 0.0, np.array((np.inf, np.inf)), (scales[0], scales[-1])
    while len(scales[firstPointIdx:lastPointIdx]) >= minSample:

        x, y = scales[firstPointIdx:lastPointIdx], counts[firstPointIdx:lastPointIdx]
        regModel = OLS(endog=y, exog=add_constant(x)).fit()
        r2score, boxCntDim, slopeCI = regModel.rsquared, regModel.params[1], regModel.conf_int(alpha=alphaCI)[1]
        minMaxLens = (x[0], x[-1])
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

        if saveFig:
            boxCntDimsDir = f"{outDir}/boxCntDims"
            if not isdir(boxCntDimsDir):
                if not isdir(outDir):
                    mkdir(outDir)
                mkdir(boxCntDimsDir)
            plt.savefig(f"{boxCntDimsDir}/{npName}_boxCntDim.png", bbox_inches='tight')
        if showPlot:
            plt.show()

        if trimLen:
            if removeSmallBoxes:
                if round(r2score, 3) < round(r2scorePrev, 3):
                    removeSmallBoxes = False
                lastPointIdx -= 1
            else:
                if round(r2score, 3) < round(r2scorePrev, 3):
                    if verbose:
                        print(f"  D_Box: {boxCntDimPrev:.4f} [{slopeCIPrev[0]:.4f}, {slopeCIPrev[1]:.4f}],  R2: {r2scorePrev:.4f},  boxLens: ({minMaxLensPrev[0]:.4f}, {minMaxLensPrev[1]:.4f})\n")
                    return r2scorePrev, boxCntDimPrev, slopeCIPrev, minMaxLensPrev
                firstPointIdx += 1
        else:
            break
        r2scorePrev, boxCntDimPrev, slopeCIPrev, minMaxLensPrev = r2score, boxCntDim, slopeCI, minMaxLens

    if verbose:
        print(f"  D_Box: {boxCntDim:.4f} [{slopeCI[0]:.4f}, {slopeCI[1]:.4f}],  R2: {r2score:.4f},  boxLens: ({minMaxLens[0]:.4f}, {minMaxLens[1]:.4f})\n")
    return r2score, boxCntDim, slopeCI, minMaxLens


# @annotate('runCase', color='cyan')
# @estDuration
def runBoxCnt(inpFilePath, 
              radType='atomic', radMult=1.2, calcBL=False, findSurfAlg='alphaShape', alphaMult=2.0, bulkCN=12,
              outDir='outputs', trimLen=True, minSample=6, confLvl=95, 
              rmInSurf=True, vis=True, figType='paper', saveFig=False, showPlot=False, verbose=False,  
              voxelSurf=True, numPoints=10000, gridNum=1024, fastbcPath='$FASTBC', genPCD=False,
              exactSurf=True, minLenMult=0.25, maxLenMult=1, numCPUs=8, numBoxLen=10, bufferDist=5.0, writeBox=True): 
    """
    Run box-counting algorithm on the surface of a given atomistic object consisting of a set of spheres represented as either a voxelised point cloud or mathematically precise object.
    
    Parameters
    ----------
    inpFilePath : str
        Path to xyz file containing Cartesian coordinates of a set of atoms.
    radType : {'atomic', 'metallic'}, optional
        Type of radii to use for the atoms.
    radMult : Union[int, float], optional
        Multiplier to the radii of atoms to identify their neighbouring atoms.
    calcBL : bool, optional
        Whether to compute the average distance from its neighbours for each atom.
    findSurfAlg : {'alphaShape', 'convexHull', 'numNeigh'}, optional
        Algorithm to identify the surface atoms.
    alphaMult : Union[int, float], optional
        Multiplier to the minimum radius to decide 'alpha' value for the alpha shape algorithm, only used if
        'findSurfAlg' is 'alphaShape'. Recommendation: 
        2.0 * 100% ATOMIC_RAD == 5/3 * 120% ATOMIC_RAD ~= 100% METALLIC_RAD * 2.5
    bulkCN : int, optional
        Minimum number of neighbouring atoms for non-surface atoms.
    outDir : str, optional
        Path to directory to store the output files.
    trimLen : bool, optional
        Whether to remove the box counts obtained using boxes of extreme sizes.
    minSample : int, optional
        Minimum number of data points to retain for slope estimation from the linear regression fitting.
    confLvl : Union[int, float], optional
        Confidence level of confidence intervals (%).
    rmInSurf : bool, optional
        Whether to remove the inner surface points.
    vis : bool, optional
        Whether to generate files for visualisation.
    figType : {'paper', 'poster', 'talk', 'notebook'}
        Research purpose of the figures generated.
    saveFig : bool, optional
        Whether to save the figures generated from linear regression fitting, only used if 'vis' is True.
    showPlot : bool, optional
        Whether to show the figures generated from linear regression fitting, only used if 'vis' is True.
    verbose : bool, optional
        Whether to display the details.
    voxelSurf : bool, optional
        Whether to represent the surface as voxelised point clouds.
    numPoints : int, optional
        Number of surface points to generate around each atom.
    gridNum : int, optional
        Resolution of the 3D binary image.
    fastbcPath : str, optional
        Path to the compiled C++ file for box-counting on 3D binary image written by Ruiz de Miras et al.
    genPCD : bool, optional
        Whether to generate point cloud data (pcd) file.
    exactSurf : bool, optional
        Whether to represent the surface in a mathematically exact manner.
    minLenMult : float, optional
        Multiplier to the minimum radius to determine the minimum box length.
    maxLenMult : float, optional
        Multiplier to the maximum radius to determine the maximum box length.
    numCPUs : int, optional
        Number of cores to be used for parallelisation.
    numBoxLen : int, optional
        Number of box length samples for the collection of the box count data, spaced evenly on logarithmic scale.
    bufferDist : Union[int,float]
        Buffer distance from the borders of the largest box (Angstrom).
    writeBox : bool, optional
        Whether to generate output file containing coordinates of examined boxes.
    
    Returns
    -------
    r2VX : float
        Coefficient of determination from linear regression fitting to the box-counting data obtained from the voxelised point cloud surface representation.
    bcDimVX : float
        Box-counting dimension of the voxelised point cloud representation of the surface.
    confIntVX : 1D ndarray of floats
        Confidence interval of the slope estimated for the voxelised point cloud surface representation.
    minMaxLensVX : tuple of floats
        Minimum and maximum box lengths for the final slope determination for the voxelised point cloud surface representation.
    r2EX : float
        Coefficient of determination from linear regression fitting to the box-counting data obtained from the mathematically exact surface representation.
    bcDimEX : float
        Box-counting dimension of the mathematically exact representation of the surface.
    confIntEX : 1D ndarray of floats
        Confidence interval of the slope estimated for the mathematically exact surface representation.
    minMaxLensEX : tuple of floats
        Minimum and maximum box lengths for final slope determination for the mathematically exact surface representation.
    
    Examples
    --------
    >>> r2VX, bcDimVX, confIntVX, minMaxLensVX, r2EX, bcDimEX, confIntEX, minMaxLensEX = runBoxCnt('example.xyz')
    """
    atomsEle, atomsRad, atomsXYZ, maxRange, minXYZ, maxXYZ = readInp(inpFilePath, radType)
    atomsNeighIdxs, atomsAvgBondLen = findNN(atomsRad, atomsXYZ, minXYZ, maxXYZ, atomsRad.max(), radMult, calcBL)
    atomsSurfIdxs = findSurf(atomsXYZ, atomsNeighIdxs, findSurfAlg, alphaMult * atomsRad.min(), bulkCN)
    testCase = inpFilePath.split('/')[-1][:-4]
    if verbose:
        print(f"\n{testCase}")

    r2VX, bcDimVX, confIntVX, minMaxLensVX = np.nan, np.nan, (np.nan, np.nan), (np.nan, np.nan)
    r2EX, bcDimEX, confIntEX, minMaxLensEX = np.nan, np.nan, (np.nan, np.nan), (np.nan, np.nan)
    if voxelSurf:
        scalesVX, countsVX = voxelBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                          testCase, outDir, numCPUs, fastbcPath,
                                          radType, numPoints, gridNum,
                                          rmInSurf, vis, verbose, genPCD)
        r2VX, bcDimVX, confIntVX, minMaxLensVX = findSlope(scalesVX, countsVX, f"{testCase}_VX", outDir, trimLen,
                                                           minSample, confLvl, vis, figType, saveFig, showPlot, verbose)
    if exactSurf:
        minAtomRad = atomsRad.min()
        scalesEX, countsEX = exactBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                                          maxRange, (minAtomRad * minLenMult, minAtomRad * maxLenMult),
                                          minXYZ, testCase, outDir, numCPUs, numBoxLen, bufferDist,
                                          rmInSurf, writeBox, verbose)
        r2EX, bcDimEX, confIntEX, minMaxLensEX = findSlope(scalesEX, countsEX, f"{testCase}_EX", outDir, trimLen,
                                                           minSample, confLvl, vis, figType, saveFig, showPlot, verbose)
    return r2VX, bcDimVX, confIntVX, minMaxLensVX, r2EX, bcDimEX, confIntEX, minMaxLensEX
