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

### To be Done
* Set path for exeDir.
* Publish to Conda.
* Nested multiprocessing.
* Better looking plots, allow figure size to be specified, allow choice for 'paper' and 'presentation'.
* Consider transforming xyz coordinates when atoms are read in to avoid using minXYZ repetitively in `scanAtom()`.

## Installation

Use `pip` or `conda` (yet to be implemented) to install `Sphractal`:

```bash
$ pip install sphractal
```
```bash
$ conda install -c conda-forge sphractal
```

`Sphractal` requires a C++ code to be compiled for the functionalities related to point clouds surface representation 
to work. This could be done by first changing into the director containing the C++ source code: 

```bash
$ cd {SPHRACTAL_DIR_PATH}/src/fbc/
```

And then compile either of the two file using respective C++ compiler. 
The second option is only viable for machines with `CUDA` platform available.

```bash
$ g++ 3DbinImBCcpu.cpp bcCPU.cpp -o {SPHRACTAL_DIR_PATH}/bin/3DbinImBCcpu.exe
```
```bash
$ nvcc -O3 bcCUDA3D.cu 3DbinImBCgpu.cpp -o {SPHRACTAL_DIR_PATH}/bin/3DbinImBCgpu.exe
```

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
