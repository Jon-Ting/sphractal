# Sphractal

[![ci-cd](https://github.com/Jon-Ting/sphractal/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Jon-Ting/sphractal/actions/workflows/ci-cd.yml)

## Description

`Sphractal` is a package that provides functionality to estimate the fractal dimension of complex 3D surfaces formed 
from overlapping spheres via box-counting algorithm. 

## Features

### Current
* Representation of the surface as either point clouds or exact surfaces.
* Efficient algorithm for 3D box-counting calculations.
* Customisable parameters to control the level of detail and accuracy of the calculation.

### Under Development
* Nested multiprocessing (boxLenConc=True).
* Transformation of xyz coordinates when atoms are read in to avoid using minXYZ repetitively in `scanAtom()`.
* Integration of C++ code for point cloud surface representation into the package.

## Installation

Use `pip` or `conda` to install `Sphractal`:

```bash
$ pip install sphractal
```
```bash
$ conda install -c conda-forge sphractal
```

### Special Requirement for Point Cloud Surface Representation
`Sphractal` requires an executable compiled from another freely available repository for the functionalities related 
to point clouds surface representation to operate properly. 

This could be done by:

* Downloading the source code from the [repository](https://github.com/Jon-Ting/fastBC.git) to a directory of your choice:
```bash
git clone https://github.com/Jon-Ting/fastBC.git
```

* Building an executable by doing either one of the following compilations according to the instructions on the [README.md](https://github.com/Jon-Ting/fastBC/blob/main/README.md) page. This will decide whether you will be running the box counting algorithm with GPU acceleration. Feel free to rename the executables to any other sensible names:
```bash
$ g++ 3DbinImBCcpu.cpp bcCPU.cpp -o 3DbinImBCcpu.exe
```
```bash
$ nvcc -O3 3DbinImBCgpu.cpp bcCUDA3D.cu -o 3DbinImBCgpu.exe
```

* (Optional) Setting the path to the executable as an environment variable accessible by Python (replace `PATH_TO_EXE` by the absolute path to the executable file you just built), otherwise you could always pass the path to the executable to the relevant functions:
```bash
$ export FASTBC_EXE={PATH_TO_EXE}
```
Note that for the environment variable to be persistent (to still exist after the terminal is closed), the line should be added to your `~/.bashrc`.

## Usage

```python
from sphractal import getExampleDataPath, runBoxCnt

xyzFilePath = getExampleDataPath()  # Replace with the path to your xyz or lmp file
boxCntResults = runBoxCnt(xyzFilePath)
```

Check out the [notebook tutorial](example.ipynb) for more detailed examples!

## Documentation

Detailed documentation and usage examples are hosted by [Read the Docs](https://sphractal.readthedocs.io/en/latest/).

## Contributing

`Sphractal` appreciates your enthusiasm and welcomes your expertise! 

Please check out the [contributing guidelines](https://github.com/Jon-Ting/sphractal/blob/main/CONTRIBUTING.md) and 
[code of conduct](https://github.com/Jon-Ting/sphractal/blob/main/CONDUCT.md). 
By contributing to this project, you agree to abide by its terms.

## License

The project is distributed under an [MIT License](https://github.com/Jon-Ting/sphractal/blob/main/LICENSE).

## Credits

The package was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) using the 
`py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Contact

Email: `Jonathan.Ting@anu.edu.au`/`jonting97@gmail.com`

Feel free to reach out if you have any questions, suggestions, or feedback.
