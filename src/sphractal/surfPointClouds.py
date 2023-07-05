from math import cos, pi, sin, sqrt
from os import mkdir
from os.path import isdir

from sphractal.constants import ATOMIC_RAD_DICT
from sphractal.utils import dist, np, oppositeInnerAtoms


def fibonacciSphere(numPoint, sphereRad):
    """Generate evenly spread numSample points on the surface of a sphere with radius sphereRad."""
    xyzs = []
    phi = pi * (sqrt(5) - 1)  # Golden angle (radians)
    for i in range(numPoint):
        y = 1 - (i / float(numPoint - 1)) * 2  # y \in [1, -1]
        radius = sqrt(1 - y*y)  # Radius at y
        theta = phi * i  # Golden angle increment
        x = cos(theta) * radius
        z = sin(theta) * radius
        xyzs.append(np.array((x*sphereRad, y*sphereRad, z*sphereRad)))
    return xyzs


def withinNeighRad(surfPointXYZ, atom1, atoms):
    """Check if surfPointXYZ falls within the radius of a neighbouring atom of atom1."""
    for neighIdx in atom1.neighs:
        atom2 = atoms[neighIdx]
        if dist((atom2.X, atom2.Y, atom2.Z), surfPointXYZ) <= ATOMIC_RAD_DICT[atom2.ele]:
            return True
    return False


def pointsOnAtom(atom1, atoms, numSample, rmInSurf=True):
    """Generate points around atom1 and classify them as either inner or outer surface."""
    surfPoints = fibonacciSphere(numSample, ATOMIC_RAD_DICT[atom1.ele])
    outerSurfs, innerSurfs = [], []
    for surfPoint in surfPoints:
        surfPointXYZ = surfPoint + np.array((atom1.X, atom1.Y, atom1.Z))
        if withinNeighRad(surfPointXYZ, atom1, atoms):
            continue
        if (not rmInSurf) or (rmInSurf and oppositeInnerAtoms(surfPointXYZ, atom1, atoms)):
            outerSurfs.append(surfPointXYZ)
        else:
            innerSurfs.append(surfPointXYZ)
    return outerSurfs, innerSurfs


def pointsToVoxels(pointXYZs, gridSize, writeFileDir):
    """Turn coordinates of point clouds into coordinates of occupied voxels."""
    # Get segmenting points in 3D space
    rangeXYZ = pointXYZs.ptp(0)
    minXYZs = np.min(pointXYZs, 0) - (max(rangeXYZ) - rangeXYZ) * 0.5
    maxXYZs = np.max(pointXYZs, 0) + (max(rangeXYZ) - rangeXYZ) * 0.5
    segmentXYZs = tuple(np.linspace(minXYZs[axis], maxXYZs[axis], num=(gridSize + 1)) for axis in range(3))

    # Get the index of the segment that each point lies within
    voxelXs = np.clip(np.searchsorted(segmentXYZs[0], pointXYZs[:, 0]) - 1, 0, gridSize)
    voxelYs = np.clip(np.searchsorted(segmentXYZs[1], pointXYZs[:, 1]) - 1, 0, gridSize)
    voxelZs = np.clip(np.searchsorted(segmentXYZs[2], pointXYZs[:, 2]) - 1, 0, gridSize)

    # Get indices of occupied voxels after flattened
    voxelIdxs = set(np.ravel_multi_index((voxelXs, voxelYs, voxelZs), (gridSize, gridSize, gridSize)))
    with open(f"{writeFileDir}/surfVoxelIdxs.txt", 'w') as f:
        for idx in voxelIdxs:
            f.write(f"{idx}\n")
    return np.column_stack((voxelXs, voxelYs, voxelZs)), voxelIdxs


def writePCD(writeFileDir, npName, surfPointXYZs):
    """Output format useful for 3D box counting using MATLAB code by Kazuaki Iida"""
    surfPointsDir = f"{writeFileDir}/surfPoints"
    if not isdir(surfPointsDir):
        mkdir(surfPointsDir)
    with open(f"{surfPointsDir}/{npName}_surfPoints.pcd", 'w') as f:
        f.write('# .PCD v.7 - Point Cloud Data file format\nVERSION .7')
        f.write('\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\n')
        f.write(f"WIDTH {len(surfPointXYZs)}\nHEIGHT 1\nPOINTS {len(surfPointXYZs)}\nDATA ascii\n")
        for xyz in surfPointXYZs:
            f.write(f"{xyz[0]} {xyz[1]} {xyz[2]}\n")


def writeSurfPoints(writeFileDir, npName, atoms, surfPointXYZs, nonSurfPointXYZs):
    surfPointsDir = f"{writeFileDir}/surfPoints"
    if not isdir(surfPointsDir):
        mkdir(surfPointsDir)
    surfAtoms = tuple((atom.X, atom.Y, atom.Z, atom.ID) for atom in atoms if atom.isSurf)
    with open(f"{surfPointsDir}/{npName}_surfPoints.xyz", 'w') as f:
        f.write(f"{len(surfPointXYZs) + len(nonSurfPointXYZs) + len(surfAtoms)}\n\n")
        for (i, xyz) in enumerate(surfPointXYZs):
            f.write(f"OU {xyz[0]} {xyz[1]} {xyz[2]} {i}\n")
        for (i, xyz) in enumerate(nonSurfPointXYZs):
            f.write(f"IN {xyz[0]} {xyz[1]} {xyz[2]} {i}\n")
        for xyz in surfAtoms:
            f.write(f"SU {xyz[0]} {xyz[1]} {xyz[2]} {xyz[3]}\n")


def writeSurfVoxels(writeFileDir, npName, surfVoxelXYZs):
    surfVoxelsDir = f"{writeFileDir}/surfVoxels"
    if not isdir(surfVoxelsDir):
        mkdir(surfVoxelsDir)
    with open(f"{surfVoxelsDir}/{npName}_surfVoxels.xyz", 'w') as f:
        f.write(f"{len(surfVoxelXYZs)}\n\n")
        for (i, xyz) in enumerate(surfVoxelXYZs):
            f.write(f"VX {xyz[0]} {xyz[1]} {xyz[2]} {i}\n")


def genSurfPoints(atoms,
                  npName, writeFileDir,
                  numPoint=300, gridNum=1024,
                  rmInSurf=True, vis=False, verbose=False, genPCD=False):
    """Generate point clouds approximating the outer spherical surface formed by a set of atoms."""
    if verbose:
        print(f"  Approximating the surface with {numPoint} point clouds for each atom...")

    surfPointXYZs, nonSurfPointXYZs = [], []
    for atom1 in atoms:
        if not atom1.isSurf:
            continue
        outerSurfs, innerSurfs = pointsOnAtom(atom1, atoms, numPoint, rmInSurf=rmInSurf)
        surfPointXYZs.extend(outerSurfs)
        nonSurfPointXYZs.extend(innerSurfs)

    surfVoxelXYZs, surfVoxelIdxs = pointsToVoxels(np.array(surfPointXYZs), gridNum, writeFileDir)
    if verbose:
        print(f"  {len(surfPointXYZs)} surface points -> {len(surfVoxelIdxs)} voxels, # grids: {gridNum}")
    if genPCD:
        writePCD(writeFileDir, npName, surfPointXYZs)
    if vis:
        writeSurfPoints(writeFileDir, npName, atoms, surfPointXYZs, nonSurfPointXYZs)
        writeSurfVoxels(writeFileDir, npName, surfVoxelXYZs)
