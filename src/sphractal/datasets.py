from importlib.resources import files
from os import listdir


def getExampleDataPath():
    """Get path to exampleOT.xyz (an octahedron palladium nanoparticle).

    Returns
    -------
    str
        Path to example file.
    """
    return str(files('sphractal.data').joinpath('exampleOT.xyz'))


def getBenchmarkDataPaths():
    """Get paths to benchmark data files.

    Returns
    -------
    exampleFiles : list of str
        Paths to example files.
    """
    dataDir = str(files('sphractal.data'))
    exampleFiles = []
    for fileName in listdir(dataDir):
        if 'xyz' not in fileName or 'example' in fileName:
            continue
        exampleFiles.append(f"{dataDir}/{fileName}")
    return exampleFiles

