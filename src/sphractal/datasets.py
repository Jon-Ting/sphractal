from importlib.resources import files
from os import listdir


def getExampleDataPath():
    """Get path to an example xyz file (an octahedron palladium nanoparticle).

    Returns
    -------
    xyzFilePath : str
        Path to xyz file.
    """
    xyzFilePath = str(files('sphractal.data').joinpath('exampleOT.xyz'))
    return xyzFilePath


def getStrongScalingDataPath():
    """Get path to the xyz file used for strong scaling tests (a sphere palladium nanoparticle with a diameter of 10 nm).

    Returns
    -------
    xyzFilePath : str
        Path to xyz file.
    """
    return str(files('sphractal.data').joinpath('strongScalingSP.xyz'))
    return xyzFilePath


def getWeakScalingDataPaths():
    """Get paths to the xyz files used for weak scaling tests (spherical palladium nanoparticles with varying diameters).

    Returns
    -------
    xyzFilePaths : list of str
        Paths to xyz files.
    """
    dataDir = str(files('sphractal.data'))
    xyzFilePaths = []
    for fileName in listdir(dataDir):
        if 'weakScaling' in fileName:
            xyzFilePaths.append(f"{dataDir}/{fileName}")
    return xyzFilePaths


def getValidationDataPath():
    """Get path to the xyz file used for validation (a file containing a single palladium atom).

    Returns
    -------
    xyzFilePath : str
        Path to xyz file.
    """
    xyzFilePath = str(files('sphractal.data').joinpath('singleAtom.xyz'))
    return xyzFilePath


def getCaseStudyDataPaths():
    """Get paths to the xyz files used for case study (ordered and disordered octahedron, rhombic dodecahedron, and tetrahedron palladium nanoparticles).

    Returns
    -------
    xyzFilePaths : list of str
        Paths to xyz files.
    """
    dataDir = str(files('sphractal.data'))
    xyzFilePaths = []
    for fileName in listdir(dataDir):
        if 'caseStudy' in fileName:
            xyzFilePaths.append(f"{dataDir}/{fileName}")
    return xyzFilePaths

