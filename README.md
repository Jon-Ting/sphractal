# Sphractal

[![ci-cd](https://github.com/Jon-Ting/sphractal/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Jon-Ting/sphractal/actions/workflows/ci-cd.yml)

## Description

`Sphractal` is a package that provides functionalities to estimate the fractal dimension of complex 3D surfaces formed from overlapping spheres via box-counting algorithm. 

## Background
* Atomic objects in molecular and nanosciences such are often represented as collection of spheres with radii associated with the atomic radius of the individual component.

![](https://raw.githubusercontent.com/Jon-Ting/sphractal/main/docs/figs/example.png)

* Some examples of these objects (inclusive of both fine- and coarse-grained representation of the individual components) 
are small molecules, proteins, nanoparticles, polymers, and porous materials such as zeolite, metal-organic framework (MOFs).
* The overall properties of these objects are often significantly influenced by their surface properties, in particular the surface area available for interaction with other entities, which is related to the surface roughness.
* Fractal dimension allows the surface complexity/roughness of objects to be measured quantitatively.
* The fractal dimension could be estimated by applying the box-counting algorithm on surfaces represented as either:
  * approximated point cloud:

![](https://raw.githubusercontent.com/Jon-Ting/sphractal/main/docs/figs/exampleVXpointCloudSliced.png)

  * that are subsequently voxelised:

![](https://raw.githubusercontent.com/Jon-Ting/sphractal/main/docs/figs/exampleVXvoxelsSliced.png)

  * or mathematically exact surfaces:

![](https://raw.githubusercontent.com/Jon-Ting/sphractal/main/docs/figs/exampleSliced.png)

## Features

### Aims
* Representation of the surface as either voxelised point clouds or mathematically exact surfaces.
* Efficient algorithm for 3D box-counting calculations.
* Customisable parameters to control the level of detail and accuracy of the calculation.

## Installation

Use `pip` or `conda` to install `Sphractal`:

```bash
pip install sphractal
```
```bash
conda install -c conda-forge sphractal
```

### Special Requirement for Point Cloud Surface Representation
`Sphractal` requires a file compiled from another freely available repository for the functionalities related to voxelised point clouds surface representation to operate properly. 

This could be done by:

* Downloading the source code from the [repository](https://github.com/Jon-Ting/fastbc.git) to a directory of your choice:
```bash
git clone https://github.com/jon-ting/fastbc.git
```

* Compile the code into an executable file (which works on any operating system) by doing either one of the following compilations according to the instructions on the [README.md](https://github.com/Jon-Ting/fastBC/blob/main/README.md) page. This will decide whether you will be running the box counting algorithm with GPU acceleration. Feel free to rename the output file from the compilation:
```bash
g++ 3DbinImBCcpu.cpp bcCPU.cpp -o 3DbinImBCcpu
```
```bash
nvcc -O3 3DbinImBCgpu.cpp bcCUDA3D.cu -o 3DbinImBCgpu
```

* (Optional) Setting the path to the compiled file as an environment variable accessible by Python (replace `<PATH_TO_FASTBC>` by the absolute path to the executable file you just built), otherwise you could always pass the path to the compiled file to the relevant functions:
```bash
export FASTBC=<PATH_TO_FASTBC>
```
Note that for the environment variable to be persistent (to still exist after the terminal is closed), the line should be added to your `~/.bashrc`.

## Usage

```python
from sphractal import getExampleDataPath, runBoxCnt

inpFile = getExampleDataPath()  # Replace with the path to your xyz or lmp file
boxCntResults = runBoxCnt(inpFile)
```

Check out the [basic demonstration](https://github.com/Jon-Ting/sphractal/blob/main/docs/basicDemo.ipynb) and [application demonstration](https://github.com/Jon-Ting/sphractal/blob/main/docs/applicationsDemo.ipynb) notebooks for further explanations and demonstrations!

## Documentation

Detailed [documentations](https://sphractal.readthedocs.io/en/latest/) are hosted by `Read the Docs`.

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
The speeding up of the inner functions via just-in-time compilations with [Numba](https://numba.pydata.org/) was inspired by the advice received during the [NCI-NVIDIA Open Hackathon 2023](https://opus.nci.org.au/display/Help/NCI-NVIDIA+Open+Hackathon+2023).

## Contact

Email: `Jonathan.Ting@anu.edu.au`/`jonting97@gmail.com`

Feel free to reach out if you have any questions, suggestions, or feedback.
