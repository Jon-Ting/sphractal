import setuptools


__version__ = '0.25.2'
with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphractal",
    version=__version__,
    author="Jonathan Yik Chang Ting",
    author_email="jonting97@gmail.com",
    description="Package to estimate surface fractal dimension of 3D objects composed of overlapping spheres via box-counting algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jon-Ting/sphractal",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
)

