from math import dist
from os.path import exists, isfile

from pytest import approx, mark

from fixtures import fixture, np, egAtomsXYZ, egAtomsNeighIdxs, egAtomsSurfIdxs, egTargetAtomIdxs
from sphractal.datasets import getExampleDataPath
from sphractal.utils import getMinMaxXYZ, readXYZ, findNN, findSurf, calcDist, closestSurfAtoms, oppositeInnerAtoms
from sphractal.surfPointClouds import fibonacciSphere, pointsOnAtom, pointsToVoxels
from sphractal.surfExact import getNearFarCoord, scanBox, writeBoxCoords, findTargetAtoms
from sphractal.boxCnt import getVoxelBoxCnts, getSphereBoxCnts, findSlope
from sphractal import runBoxCnt


EG_XYZ_ATOM_NUM = 670


@fixture
def egMinMaxXYZ():
    return np.array([404.065, 404.065, 404.065]), np.array([440.65, 440.65, 440.65]) 


@fixture
def egAtomsEle():
    return np.array(['Pd']*EG_XYZ_ATOM_NUM, dtype='U2')


@fixture
def egAtomsRad():
    return np.array([1.69]*EG_XYZ_ATOM_NUM)


@fixture
def egBoxCntDims():
    return (0.9967, 2.1778, (2.0038, 2.3517), 0.9971, 2.3454, (2.2183, 2.4725))


@fixture
def egVoxelBoxCnts():
    return ([-2.70926996, -2.40823997, -2.10720997, -1.80617997, -1.50514998, -1.20411998, -0.90308999, -0.60205999, -0.30103], 
            [0.90308999, 1.50514998, 2.30963017, 2.91855453, 3.49192171, 4.05419158, 4.47568571, 4.51703746, 4.52071928])


@fixture
def egSphereBoxCnts():
    return ([-0.23688234, -0.16309612, -0.10004438, -0.03477764,  0.03932408, 0.10260591,  0.17060299,  0.24023892,  0.30488175,  0.37314659], 
            [3.20194306, 3.32139128, 3.5171959 , 3.68142216, 3.80522891, 3.9531796 , 4.09272064, 4.27207379, 4.38937875, 4.52953301])


def test_getExampleDataPath():
    """Unit test of getExampleDataPath()."""
    xyzFilePathAct = getExampleDataPath()

    assert isinstance(xyzFilePathAct, str), 'getExampleDataPath did not return a string'

    assert exists(xyzFilePathAct), 'example.xyz not found'
    assert isfile(xyzFilePathAct), 'example.xyz is not a file'


@mark.parametrize('radType, atomRad', [('atomic', 1.69), ('metallic', 1.37)])
def test_readXYZ(radType, atomRad, egAtomsEle, egAtomsXYZ):
    """Unit test of readXYZ()."""
    atomsEleAct, atomsRadAct, atomsXYZAct, maxRangeAct, minXYZAct, maxXYZAct = readXYZ(getExampleDataPath(), radType)

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


@mark.parametrize('maxAtomRad, radMult, totNeighNumExp, avgAvgBL', [(1.69, 1.2, 6840, 2.87438906), (1.37, 1.5, 8820, 3.12820867)])
def test_findNN(maxAtomRad, radMult, totNeighNumExp, avgAvgBL, egMinMaxXYZ, egAtomsXYZ, egAtomsNeighIdxs):
    """Unit test of findNN()."""
    egMinXYZ, egMaxXYZ = egMinMaxXYZ
    atomsRad = np.array([maxAtomRad] * EG_XYZ_ATOM_NUM)
    atomsNeighIdxsAct, atomsAvgBondLensAct = findNN(atomsRad, egAtomsXYZ, egMinXYZ, egMaxXYZ, maxAtomRad, radMult, True)
    totNeighNumAct = sum([len(atomNeighIdxs[atomNeighIdxs > -1]) for atomNeighIdxs in atomsNeighIdxsAct])

    assert isinstance(atomsNeighIdxsAct, np.ndarray), 'atomsNeighIdxs not ndarray'
    assert isinstance(atomsAvgBondLensAct, np.ndarray), 'atomsAvgBondLens not ndarray'

    assert totNeighNumAct == totNeighNumExp, 'Incorrect atomsNeighIdxs values'
    assert atomsAvgBondLensAct.mean() == approx(avgAvgBL), 'Incorrect atomsAvgBondLens values'


@mark.parametrize('findSurfOption, numSurfAtomsExp', [('alphaShape', 326), ('convexHull', 6), ('numNeigh', 326)])
def test_findSurf(findSurfOption, numSurfAtomsExp, egAtomsXYZ, egAtomsNeighIdxs):
    """Unit test of findSurf()."""
    atomsSurfIdxsAct = findSurf(egAtomsXYZ, egAtomsNeighIdxs, findSurfOption, alpha=2.0 * 1.69)

    assert isinstance(atomsSurfIdxsAct, np.ndarray), 'atomsSurfIdxs not ndarray'

    assert len(atomsSurfIdxsAct) == numSurfAtomsExp, 'Incorrect surface atom indices'


def test_calcDist(egAtomsXYZ):
    """Unit test of calcDist()."""
    distsAct, distsExp = np.empty((EG_XYZ_ATOM_NUM, EG_XYZ_ATOM_NUM)), np.empty((EG_XYZ_ATOM_NUM, EG_XYZ_ATOM_NUM))
    for (i, p1) in enumerate(egAtomsXYZ):
        for (j, p2) in enumerate(egAtomsXYZ):
            distsAct[i][j] == calcDist(p1, p2)
            distsAct[i][j] == dist(p1, p2)
    assert distsAct == approx(distsExp), 'Incorrect distance from calcDist()'


#@mark.parametrize('pointXYZ, surfNeighIdxs, idxPairExp', [(), (), ()])
#def test_closestSurfAtoms(pointXYZ, idxPairExp, egAtomsXYZ, egAtomsNeighIdxs):
#    """Unit test of closestSurfAtoms(). (To be implemented)"""
#    idxPairAct = closestSurfAtoms(pointXYZ, surfNeighIdxs, egAtomsXYZ, egAtomsNeighIdxs)
#    assert idxPairAct == idxPairExp, 'Incorrect atom indices pairs from closestSurfAtoms()'


#@mark.parametrize('pointXYZ, atom1XYZ, atomNeighIdxs, isOppExp', [(), (), ()])
#def test_oppositeInnerAtoms(pointXYZ, atom1XYZ, atomNeighIdxs, isOppExp, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs):
#    """Unit test of oppositeInnerAtoms(). (To be implemented)"""
#    isOppAct = oppositeInnerAtoms(pointXYZ, atom1XYZ, atomNeighIdxs, 
#                                  egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs)
#    assert isOppAct == isOppExp, 'Incorrect results from oppositeInnerAtoms()'


@mark.parametrize('numPoint, sphereRad, xyzsExp', 
    [(3, 1.0, np.array([[0., 1., 0.], [-0.73736888, 0., -0.67549029], [0., -1., 0.]])), 
     (5, 1.5, np.array([[0., 1.5, 0.], [-0.95787027, 0.75, -0.87748763], [0.13113859, 0., 1.49425656], [0.79038527, -0.75, -1.03091762], [-0., -1.5, 0.]])), 
     (2, 100, np.array([[0., 100., 0.], [-0., -100., -0.]]))])
def test_fibonacciSphere(numPoint, sphereRad, xyzsExp):
    """Unit test of fibonacciSphere()."""
    xyzsAct = fibonacciSphere(numPoint, sphereRad)

    assert isinstance(xyzsAct, np.ndarray), 'Incorrect data type from fibonacciSphere()'
    assert xyzsAct == approx(xyzsExp), 'Incorrect coordinates from fibonacciSphere()'


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
#
#    assert len(voxelIdxs) == numVoxelsExp, 'Incorrect number of voxels'


#@mark.parametrize('scanBoxIdx, atomCoord', [(), (), ()])
#def test_getNearFarCoord(scanBoxIdx, atomCoord, scanBoxNearFarExp):
#    """Unit test of getNearFarCoord(). (To be implemented)"""
#    scanBoxNearFarAct = getNearFarCoord(scanBoxIdx, scanBoxLen, lowBound, atomCoord)
#    assert scanBoxNearFarAct == approx(scanBoxNearFarExp), 'Incorrect coordinates from getNearFarCoord()' 


#def test_scanBox():
#    """Unit test of scanBox(). (To be implemented)"""
#    belongTest = scanBox(minXYZ, scanBoxIdxs, scanBoxNearFarXYZs, scanBoxLen,
#                 atomIdx, atomRad, atomXYZ, atomNeighIdxs,
#                 atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
#                 rmInSurf=True)


#def test_writeBoxCoords(egAtomsEle, egAtomsXYZ, egBoxs, egMinMaxXYZ):
#    """Unit test of writeBoxCoords(). (To be implemented)"""
#    writeBoxCoords(egAtomsEle, egAtomsXYZ, egBoxs[0], egBoxs[1], egMinMaxXYZ[0], egBoxs[3], '.', 'example')
#    assert exists('./boxCoords/example_boxCoords.xyz'), 'Could not find example_boxCoords.xyz'
#    assert isfile('./boxCoords/example_boxCoords.xyz'), 'example_boxCoords.xyz is not a file'


def test_findTargetAtoms(egAtomsNeighIdxs, egTargetAtomIdxs):
    """Unit test of findTargetAtoms()."""
    targetAtomsIdxsAct = findTargetAtoms(egAtomsNeighIdxs)
    assert np.all(targetAtomsIdxsAct == egTargetAtomIdxs), 'Incorrect atom indices from findTargetAtoms()'


#def test_findSlope(egBoxCntDims):
#    """Unit test of findSlope()."""
#    boxCntDimsAct = findSlope(scaleChange, cntChange, npName='example', visReg=False, saveFig=False)
#    assert boxCntDimsAct == approx(egBoxCntDims), 'Incorrect estimation of box-counting dimensions by findSlope()'


#def test_getVoxelBoxCnt(egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs, egVoxelBoxCnts):
#    """Integration test of getVoxelBoxCnts()."""
#    voxelBoxCntsAct = getVoxelBoxCnts(egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs,
#                                      'example', exeDir='.', rmInSurf=True, vis=False)
#    assert voxelBoxCntsAct == approx(egVoxelBoxCnts), 'Incorrect box-counts from getVoxelBoxCnts()'


#def test_getSphereBoxCnt(egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs, egMinMaxXYZ, egSphereBoxCnts):
#    """Integration test of getSphereBoxCnts()."""
#    sphereBoxCntsAct = getSphereBoxCnts(egAtomsEle, egAtomsRad, egAtomsSurfIdxs, egAtomsXYZ, egAtomsNeighIdxs,
#                       maxRange, minMaxBoxLens, egMinMaxXYZ[0], 'example', rmInSurf=True, writeBox=False)
#    assert sphereBoxCntsAct == approx(egSphereBoxCnts), 'Incorrect box-counts from getSphereBoxCnts()'


#def test_runBoxCnt(egBoxCntDims):
#    """Integration test of runBoxCnt()."""
#    runBoxCnt(xyzFilePath, findSurfOption='alphaShape', alphaMult=2.5, writeFileDir='.', lenRange='Trimmed',
#              rmInSurf=True, vis=True, saveFig=True, showPlot=False, verbose=False,
#              runPointCloudBoxCnt=True, numPoints=300, gridNum=1024, exeDir='.', procUnit='cpu', genPCD=False,
#              runExactSphereBoxCnt=True, minLenMult=0.25, maxLenMult=1, writeBox=False, boxLenConc=True, maxWorkers=2)
#    assert


#def test_regression(egBoxCntDims):
#    """Regression test for eg.txt."""
#    scaleChange, cntChange = runBoxCnt(getExampleDataPath())
#    assert cntChange[0] == , 'First count has changed!'
#    assert cntChange[-1] == , 'Last count has changed!'

