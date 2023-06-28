from importlib import resources


def getExampleDataPath():
    """Get path to example.xyz.

    Returns
    -------
    pathlib.PosixPath
        Path to file.
    """
    with resources.path('sphractal.data', 'example.xyz') as f:
        dataFilePath = f
    return dataFilePath
