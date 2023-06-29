from importlib.resources import files


def getExampleDataPath():
    """Get path to example.xyz (an octahedron palladium nanoparticle).

    Returns
    -------
    pathlib.PosixPath
        Path to file.
    """
    return str(files('sphractal.data').joinpath('example.xyz'))

