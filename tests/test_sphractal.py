from math import dist
# from os import environ
from os.path import exists, isdir, isfile
from shutil import rmtree

from pytest import approx, mark

from fixtures import fixture, np, egAtomsXYZ, egAtomsNeighIdxs, egAtomsSurfIdxs, egAtomsWithSurfNeighIdxs
from sphractal.datasets import getExampleDataPath, getStrongScalingDataPath, getWeakScalingDataPaths, \
    getValidationDataPath, getCaseStudyDataPaths
from sphractal.utils import estDuration, getMinMaxXYZ, readInp, findNN, findSurf, calcDist, closestSurfAtoms, \
    oppositeInnerAtoms
from sphractal.surfVoxel import fibonacciSphere, pointsOnAtom, pointsToVoxels, voxelBoxCnts
from sphractal.surfExact import getNearFarCoord, scanBox, writeBoxCoords, findAtomsWithSurfNeighs, exactBoxCnts
from sphractal.boxCnt import voxelBoxCnts, exactBoxCnts, findSlope, runBoxCnt


EG_XYZ_ATOM_NUM = 670
ATOM_RAD = 1.69
MAX_RANGE = 36.58499999999998


@fixture
def egMinMaxXYZ():
    return np.array([404.065, 404.065, 404.065]), np.array([440.65, 440.65, 440.65])


@fixture
def egAtomsEle():
    return np.array(['Pd']*EG_XYZ_ATOM_NUM, dtype='U2')


@fixture
def egAtomsRad():
    return np.array([ATOM_RAD]*EG_XYZ_ATOM_NUM)


@fixture
def egVoxelBoxCnts():
    return ([-2.70926996, -2.40823997, -2.10720997, -1.80617997, -1.50514998, -1.20411998, -0.90308999, -0.60205999, -0.30103],
            [0.90308999, 1.50514998, 2.30963017, 2.91855453, 3.49192171, 4.05419158, 4.47568571, 4.51703746, 4.52071928])


@fixture
def egExactBoxCnts():
    return ([-0.23688234, -0.16309612, -0.10004438, -0.03477764,  0.03932408, 0.10260591,  0.17060299,  0.24023892,  0.30488175,  0.37314659],
            [3.20194306, 3.32139128, 3.5171959 , 3.68142216, 3.80522891, 3.9531796 , 4.09272064, 4.27207379, 4.38937875, 4.52953301])


@fixture
def egVoxelBoxCntDims():
    return 0.99646974, 2.11889159, np.array((1.94381059, 2.29397261))


@fixture
def egExactBoxCntDims():
    return 0.99660096, 2.24426950, np.array((2.11334077, 2.37519824))


def test_estDuration(egMinMaxXYZ):
    distDuration = estDuration(dist)
    distance, duration = distDuration(egMinMaxXYZ[0], egMinMaxXYZ[1])
    assert distance == approx(63.36707879), 'Incorrect output'
    assert isinstance(duration, float), 'Incorrect duration data type'


def test_getExampleDataPath():
    """Unit test of getExampleDataPath()."""
    inpFilePathAct = getExampleDataPath()
    assert isinstance(inpFilePathAct, str), 'getExampleDataPath() did not return a string'
    assert exists(inpFilePathAct), 'exampleOT.xyz not found'
    assert isfile(inpFilePathAct), 'exampleOT.xyz is not a file'


def test_getStrongScalingDataPath():
    """Unit test of getStrongScalingDataPath()."""
    inpFilePathAct = getStrongScalingDataPath()
    assert isinstance(inpFilePathAct, str), 'getStrongScalingDataPath() did not return a string'
    assert exists(inpFilePathAct), 'strongScalingSP.xyz not found'
    assert isfile(inpFilePathAct), 'strongScalingSP.xyz is not a file'


def test_getWeakScalingDataPaths():
    """Unit test of getWeakScalingDataPaths()."""
    inpFilePathsAct = getWeakScalingDataPaths()
    assert isinstance(inpFilePathsAct, list), 'getWeakScalingDataPaths() did not return a list'
    assert isinstance(inpFilePathsAct[0], str), 'Path in list is not str'
    assert len(inpFilePathsAct) == 12, 'Incorrect number of paths returned'
    assert exists(inpFilePathsAct[0]), 'Path in list not found'
    assert isfile(inpFilePathsAct[0]), 'Path in list not a file'


def test_getValidationDataPath():
    """Unit test of getValidationDataPath()."""
    inpFilePathAct = getValidationDataPath()
    assert isinstance(inpFilePathAct, str), 'getValidationDataPath() did not return a string'
    assert exists(inpFilePathAct), 'singleAtom.xyz not found'
    assert isfile(inpFilePathAct), 'singleAtom.xyz is not a file'


def test_getCaseStudyDataPaths():
    """Unit test of getCaseStudyDataPaths()."""
    inpFilePathsAct = getCaseStudyDataPaths()
    assert isinstance(inpFilePathsAct, list), 'getCaseStudyDataPaths() did not return a list'
    assert isinstance(inpFilePathsAct[0], str), 'Path in list is not str'
    assert len(inpFilePathsAct) == 18, 'Incorrect number of paths returned'
    assert exists(inpFilePathsAct[0]), 'Path in list not found'
    assert isfile(inpFilePathsAct[0]), 'Path in list not a file'


@mark.parametrize('radType, atomRad', [('atomic', ATOM_RAD), ('metallic', 1.37)])
def test_readInp(radType, atomRad, egAtomsEle, egAtomsXYZ):
    """Unit test of readInp()."""
    atomsEleAct, atomsRadAct, atomsXYZAct, maxRangeAct, minXYZAct, maxXYZAct = readInp(getExampleDataPath(), radType)

    assert isinstance(atomsEleAct, np.ndarray), 'atomsEle not ndarray'
    assert isinstance(atomsRadAct, np.ndarray), 'atomsRad not ndarray'
    assert isinstance(atomsXYZAct, np.ndarray), 'atomsXYZ not ndarray'

    assert atomsEleAct.dtype == '<U2', 'Incorrect atomsEle data type'

    assert np.all(atomsEleAct == egAtomsEle), 'Incorrect atomsEle values'
    assert atomsRadAct == approx([atomRad]*EG_XYZ_ATOM_NUM), 'Incorrect atomsRad values'
    assert atomsXYZAct == approx(egAtomsXYZ), 'Incorrect atomsXYZ values'

    assert maxRangeAct == approx(36.58499999999998), 'Incorrect maxRange value'
    assert minXYZAct == approx([404.065, 404.065, 404.065]), 'Incorrect minXYZ values'
    assert maxXYZAct == approx([440.65, 440.65, 440.65]), 'Incorrect maxXYZ values'


@mark.parametrize('maxAtomRad, radMult, totNeighNumExp, avgAvgBL', [(ATOM_RAD, 1.2, 6840, 2.87438906), (1.37, 1.5, 9774, 3.21771150)])
def test_findNN(maxAtomRad, radMult, totNeighNumExp, avgAvgBL, egMinMaxXYZ, egAtomsXYZ, egAtomsNeighIdxs):
    """
    Unit test of findNN(). 
    calcBL=False was not tested as there's no extra code for this conditional branch. 

    TODO: Test with extreme radMult.
    """
    egMinXYZ, egMaxXYZ = egMinMaxXYZ
    atomsRad = np.array([maxAtomRad] * EG_XYZ_ATOM_NUM)
    atomsNeighIdxsAct, atomsAvgBondLensAct = findNN(atomsRad, egAtomsXYZ, egMinXYZ, egMaxXYZ, maxAtomRad, radMult, True)
    totNeighNumAct = sum([len(atomNeighIdxs[atomNeighIdxs > -1]) for atomNeighIdxs in atomsNeighIdxsAct])

    assert isinstance(atomsNeighIdxsAct, np.ndarray), 'atomsNeighIdxs not ndarray'
    assert isinstance(atomsAvgBondLensAct, np.ndarray), 'atomsAvgBondLens not ndarray'

    assert totNeighNumAct == totNeighNumExp, 'Incorrect atomsNeighIdxs values'
    assert atomsAvgBondLensAct.mean() == approx(avgAvgBL), 'Incorrect atomsAvgBondLens values'


@mark.parametrize('findSurfAlg, numSurfAtomsExp', [('alphaShape', 326), ('convexHull', 6), ('numNeigh', 326)])
def test_findSurfAlgs(findSurfAlg, numSurfAtomsExp, egAtomsXYZ, egAtomsNeighIdxs):
    """
    Unit test of findSurf() outputs for different 'findSurfAlg' options.

    TODO: Test with extreme alpha.
    """
    atomsSurfIdxsAct = findSurf(egAtomsXYZ, egAtomsNeighIdxs, findSurfAlg, alpha=2.0 * ATOM_RAD)
    assert isinstance(atomsSurfIdxsAct, np.ndarray), 'atomsSurfIdxs not ndarray'
    assert len(atomsSurfIdxsAct) == numSurfAtomsExp, 'Incorrect number of surface atoms'


def test_findSurfAcc(egAtomsXYZ, egAtomsNeighIdxs, egAtomsSurfIdxs):
    """Unit test of findSurf() outputs accuracy."""
    atomsSurfIdxsAct = findSurf(egAtomsXYZ, egAtomsNeighIdxs, alpha=2.0 * ATOM_RAD)
    assert np.all(atomsSurfIdxsAct == egAtomsSurfIdxs), 'Incorrect surface atom indices'


def test_calcDist(egAtomsXYZ):
    """Unit test of calcDist()."""
    numTests = 100
    distsAct, distsExp = np.empty((numTests, numTests)), np.empty((numTests, numTests))
    for (i, p1) in enumerate(egAtomsXYZ):
        if i >= 100:
            continue
        for (j, p2) in enumerate(egAtomsXYZ):
            if j >= 100:
                continue
            distsAct[i][j] = calcDist(p1, p2)
            distsExp[i][j] = dist(p1, p2)
    assert distsAct == approx(distsExp), 'Incorrect calculated distance'


#@mark.parametrize('pointXYZ, surfNeighIdxs, idxPairExp', [(), (), ()])
#def test_closestSurfAtoms(pointXYZ, idxPairExp, egAtomsXYZ, egAtomsNeighIdxs):
#    """Unit test of closestSurfAtoms(). (To be implemented)"""
#    idxPairAct = closestSurfAtoms(pointXYZ, surfNeighIdxs, egAtomsXYZ, egAtomsNeighIdxs)
#    assert idxPairAct == idxPairExp, 'Incorrect atom indices pairs'


#@mark.parametrize('pointXYZ, atom1XYZ, atomNeighIdxs, isOppExp', [(), (), ()])
#def test_oppositeInnerAtoms(pointXYZ, atom1XYZ, atomNeighIdxs, isOppExp, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs):
#    """Unit test of oppositeInnerAtoms(). (To be implemented)"""
#    isOppAct = oppositeInnerAtoms(pointXYZ, atom1XYZ, atomNeighIdxs, 
#                                  egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs)
#    assert isOppAct == isOppExp, 'Incorrect results'


@mark.parametrize('numPoints, sphereRad, xyzsExp',
    [(3, 1.0, np.array([[0., 1., 0.], [-0.73736888, 0., -0.67549029], [0., -1., 0.]])),
     (5, 1.5, np.array([[0., 1.5, 0.], [-0.95787027, 0.75, -0.87748763], [0.13113859, 0., 1.49425656], [0.79038527, -0.75, -1.03091762], [-0., -1.5, 0.]])),
     (2, 100, np.array([[0., 100., 0.], [-0., -100., -0.]]))])
def test_fibonacciSphere(numPoints, sphereRad, xyzsExp):
    """Unit test of fibonacciSphere()."""
    xyzsAct = fibonacciSphere(numPoints, sphereRad)
    assert isinstance(xyzsAct, np.ndarray), 'Incorrect output data type'
    assert xyzsAct == approx(xyzsExp), 'Incorrect surface point coordinates'


#@mark.parametrize('atomIdx, numOuterPointsExp, numInnerPointsExp, rmInSurf', [(), (), ()])
#def test_pointsOnAtom(atomIdx, numOuterPointsExp, numInnerPointsExp, rmInSurf, egAtomsSurfIdxs, egAtomsRad, egAtomsXYZ, egAtomsNeighIdxs):
#    """Unit test of pointsOnAtom(). (To be implemented)"""
#    outerSurfsAct, innerSurfsAct = pointsOnAtom(atomIdx, 300, egAtomsSurfIdxs, egAtomsRad, egAtomsXYZ, egAtomsNeighIdxs, None, rmInSurf)
#    assert len(outerSurfsAct) == numOuterPointsExp, 'Incorrect number of outer surface points'
#    assert len(innerSurfsAct) == numInnerPointsExp, 'Incorrect number of inner surface points'


#@mark.parametrize('gridSize, numVoxelsExp', [(1024, 33204), (512, 33168), (256, 32888), (128, 29901), (64, 11329), (32, 3104)])
#def test_pointsToVoxels(gridSize, numVoxelsExp, egPointXYZs):
#    """Unit test of pointsToVoxels(). (To be implemented)"""
#    voxelXYZs, voxelIdxs = pointsToVoxels(egPointXYZs, gridSize)
#    assert len(voxelIdxs) == numVoxelsExp, 'Incorrect number of voxels'


#@mark.parametrize('scanBoxIdx, atomCoord', [(), (), ()])
#def test_getNearFarCoord(scanBoxIdx, atomCoord, scanBoxNearFarExp):
#    """Unit test of getNearFarCoord(). (To be implemented)"""
#    scanBoxNearFarAct = getNearFarCoord(scanBoxIdx, scanBoxLen, lowBound, atomCoord)
#    assert scanBoxNearFarAct == approx(scanBoxNearFarExp), 'Incorrect coordinates' 


#def test_scanBox():
#    """Unit test of scanBox(). (To be implemented)"""
#    belongTest = scanBox(minXYZ, scanBoxIdxs, scanBoxNearFarXYZs, scanBoxLen,
#                 atomIdx, atomRad, atomXYZ, atomNeighIdxs,
#                 atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
#                 rmInSurf=True)


def test_findAtomsWithSurfNeighs(egAtomsNeighIdxs, egAtomsSurfIdxs, egAtomsWithSurfNeighIdxs):
    """Unit test of findAtomsWithSurfNeighs()."""
    atomsWithSurfNeighIdxsAct = findAtomsWithSurfNeighs(egAtomsNeighIdxs, egAtomsSurfIdxs)
    assert np.all(atomsWithSurfNeighIdxsAct == egAtomsWithSurfNeighIdxs), 'Incorrect atom indices'


@mark.parametrize('trimLen', [True, False])
@mark.parametrize('visReg', [True, False])
@mark.parametrize('saveFig, figExists', [(True, True), (False, False)])
def test_findSlopeVis(trimLen, visReg, saveFig, figExists, egExactBoxCnts):
    """Unit test of findSlope() functionalities for different 'trimLen', 'visReg', and 'saveFig' options."""
    boxCntDimsAct = findSlope(egExactBoxCnts[0], egExactBoxCnts[1], 'example_ES', 'tests/outputs', trimLen, visReg=visReg, saveFig=saveFig)
    assert exists('./tests/outputs/boxCntDims/example_ES_boxCntDim.png') == figExists, 'example_ES_boxCntDim.png is not found'
    assert isfile('./tests/outputs/boxCntDims/example_ES_boxCntDim.png') == figExists, 'example_ES_boxCntDim.png is not a file'
    if isdir('./tests/outputs'):
        rmtree('./tests/outputs')


@mark.filterwarnings('ignore')
@mark.parametrize('minSample, isFinite1', [(-99, True), (11, False)])
@mark.parametrize('confLvl, isFinite2', [(-101, False), (99.9, True), (100, False)])
def test_findSlopeConfInt(minSample, isFinite1, confLvl, isFinite2, egExactBoxCnts):
    """Unit test of findSlope() outputs for different 'minSample' and 'confLvl' values."""
    boxCntDimsAct = findSlope(egExactBoxCnts[0], egExactBoxCnts[1], minSample=minSample, confLvl=confLvl)
    assert np.all(np.isfinite(boxCntDimsAct[2])) == (isFinite1 and isFinite2), 'Incorrect confidence interval'


@mark.parametrize('scales, counts, boxCntDimsExp', [([-2.70926996, -2.40823997, -2.10720997, -1.80617997, -1.50514998, -1.20411998, -0.90308999, -0.60205999, -0.30103], [0.90308999, 1.50514998, 2.30963017, 2.91855453, 3.49192171, 4.05419158, 4.47568571, 4.51703746, 4.52071928], (0.99646974, 2.11889159, np.array((1.94381059, 2.29397261)))), ([-0.23688234, -0.16309612, -0.10004438, -0.03477764, 0.03932408, 0.10260591, 0.17060299, 0.24023892, 0.30488175, 0.37314659], [3.20194306, 3.32139128, 3.5171959 , 3.68142216, 3.80522891, 3.9531796 , 4.09272064, 4.27207379, 4.38937875, 4.52953301], (0.99660096, 2.24426950, np.array((2.11334077, 2.37519824))))])
def test_findSlopeAcc(scales, counts, boxCntDimsExp):
    """Unit test of findSlope() outputs accuracy."""
    boxCntDimsAct = findSlope(scales, counts)
    assert isinstance(boxCntDimsAct[2], np.ndarray), 'Confidence interval returned is not ndarray'
    assert len(boxCntDimsAct[2]) == 2, 'Confidence interval returned is not two numbers'
    assert np.all(boxCntDimsAct[2] == approx(boxCntDimsExp[2])), 'Incorrect estimation of box-counting dimensions by findSlope()'
    assert boxCntDimsAct[:2] == approx(boxCntDimsExp[:2]), 'Incorrect estimation of box-counting dimensions by findSlope()'


#def test_getVoxelBoxCntVis(egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs):
#    """Unit test of voxelBoxCnts() functionalities to generate output files for visualisation (To be uncommented when compiled C++ code could be shipped together)."""
#    assert isfile(os.environ['FASTBC_EXE']), 'Executable not found at FASTBC_EXE'
#    voxelScalesAct, voxelCountsAct = voxelBoxCnts(egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs,
#                                                     'example', 'tests/outputs', verbose=True, genPCD=True)
#    assert exists('./tests/outputs/surfVoxelIdxs.txt'), 'surfVoxelBoxIdxs.txt is not found'
#    assert isfile('./tests/outputs/surfVoxelIdxs.txt'), 'surfVoxelBoxIdxs.txt is a file'
#    assert exists('./tests/outputs/surfVoxelBoxCnts.txt'), 'surfVoxelBoxCnts is not found'
#    assert isfile('./tests/outputs/surfVoxelBoxCnts.txt'), 'surfVoxelBoxCnts is not a file'
#    assert exists('./tests/outputs/surfPoints/example_surfPoints.xyz'), 'example_surfPoints.xyz is not found'
#    assert isfile('./tests/outputs/surfPoints/example_surfPoints.xyz'), 'example_surfPoints.xyz is not a file'
#    assert exists('./tests/outputs/surfPoints/example_surfPoints.pcd'), 'example_surfPoints.pcd is not found'
#    assert isfile('./tests/outputs/surfPoints/example_surfPoints.pcd'), 'example_surfPoints.pcd is not a file'
#    assert exists('./tests/outputs/surfVoxels/example_surfVoxels.xyz'), 'example_surfVoxels.xyz is not found'
#    assert isfile('./tests/outputs/surfVoxels/example_surfVoxels.xyz'), 'example_surfVoxels.xyz is not a file'
#    if isdir('./tests/outputs'):
#        rmtree('./tests/outputs')


#@mark.parametrize('rmInSurf, voxelScalesExp, voxelCountsExp', [(True, [-2.70926996, -2.40823997, -2.10720997, -1.80617997, -1.50514998, -1.20411998, -0.90308999, -0.60205999, -0.30103], [0.90308999, 1.50514998, 2.30963017, 2.91855453, 3.49192171, 4.05419158, 4.47568571, 4.51703746, 4.52071928]), (False, [-2.70926996, -2.40823997, -2.10720997, -1.80617997, -1.50514998, -1.20411998, -0.90308999, -0.60205999, -0.30103], [0.90308999, 1.50514998, 2.35024802, 3.02530587, 3.62479758, 4.14640714, 4.54740546, 4.5884958, 4.59508819])])
#def test_getVoxelBoxCntAcc(rmInSurf, voxelScalesExp, voxelCountsExp, egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs):
#    """Unit test of voxelBoxCnts() outputs accuracy (To be uncommented when compiled C++ code could be shipped together)."""
#    voxelScalesAct, voxelCountsAct = voxelBoxCnts(egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs,
#                                                     'example', 'tests/outputs', rmInSurf=rmInSurf, vis=False)
#    assert voxelScalesAct == approx(voxelScalesExp), 'Incorrect scales'
#    assert voxelCountsAct == approx(voxelCountsExp), 'Incorrect box counts'


@mark.parametrize('rmInSurf, exactScalesExp, exactCountsExp', [(True, [-0.23688234, -0.16309612, -0.10004438, -0.03477764, 0.03932408, 0.10260591, 0.17060299, 0.24023892, 0.30488175, 0.37314659], [3.20194306, 3.32139128, 3.5171959, 3.68142216, 3.80522891, 3.9531796, 4.09272064, 4.27207379, 4.38937875, 4.52953301]), (False, [-0.23688234, -0.16309612, -0.10004438, -0.03477764, 0.03932408, 0.10260591, 0.17060299, 0.24023892, 0.30488175, 0.37314659], [3.49789674, 3.69055046, 3.84997191, 4.00056421, 4.18301346, 4.32281862, 4.47290265, 4.61702132, 4.74061529, 4.86194043])])
def test_getExactBoxCnt(rmInSurf, exactScalesExp, exactCountsExp, egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs, egMinMaxXYZ):
    """Unit test of exactBoxCnts()."""
    exactScalesAct, exactCountsAct = exactBoxCnts(egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs,
                                                        MAX_RANGE, (ATOM_RAD*0.25, ATOM_RAD), egMinMaxXYZ[0], 'example', 'tests/outputs', rmInSurf=rmInSurf)
    print(exactScalesAct, exactCountsAct)
    assert exactCountsAct == approx(exactCountsExp), 'Incorrect scales'
    assert exactCountsAct == approx(exactCountsExp), 'Incorrect box counts'
    assert exists('./tests/outputs/boxCoords/example_boxCoords.xyz'), 'example_boxCoords.xyz is not found'
    assert isfile('./tests/outputs/boxCoords/example_boxCoords.xyz'), 'example_boxCoords.xyz is not a file'
    if isdir('./tests/outputs'):
        rmtree('./tests/outputs')


#def test_runBoxCnt(egVoxelBoxCntDims, egExactBoxCntDims):
#    """Unit and regression test of runBoxCnt() (To be uncommented when compiled C++ code could be shipped together)."""
#    assert isfile(environ['FASTBC_EXE']), 'Executable not found at FASTBC_EXE'
#    boxCntDimsAct = runBoxCnt(getExampleDataPath(), writeFileDir='tests/outputs')
#    assert boxCntDimsAct[:2] == approx(egVoxelBoxCntDims[:2]), 'Incorrect R2 and D_Box for point clouds representation'
#    assert boxCntDimsAct[2] == approx(egVoxelBoxCntDims[2]), 'Incorrect confidence interval for point clouds representation'
#    assert boxCntDimsAct[-3:-1] == approx(egExactBoxCntDims[:2]), 'Incorrect R2 and D_Box for exact surface representation'
#    assert boxCntDimsAct[-1] == approx(egExactBoxCntDims[2]), 'Incorrect confidence interval for exact surface representation'
#    if isdir('./tests/outputs'):
#        rmtree('./tests/outputs')

