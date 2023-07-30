from importlib.resources import files
from os import listdir


def getExampleDataPath():
    """Get path to exampleOT.xyz (an octahedron palladium nanoparticle).

    Returns
    -------
    str
        Path to xyz file.
    """
    return str(files('sphractal.data').joinpath('exampleOT.xyz'))


def getStrongScalingDataPath():
    """Get path to strongScalingSP.xyz (a sphere palladium nanoparticle with a diameter of 10 nm).

    Returns
    -------
    str
        Path to xyz file.
    """
    return str(files('sphractal.data').joinpath('strongScalingSP.xyz'))


def getWeakScalingDataPaths():
    """Get paths to xyz files used for weak scaling testings.

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
    """Get path to singleAtom.xyz (a file containing a single palladium atom).

    Returns
    -------
    str
        Path to xyz file.
    """
    return str(files('sphractal.data').joinpath('singleAtom.xyz'))


def getCaseStudyDataPaths():
    """Get paths to xyz files used for case study.

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

