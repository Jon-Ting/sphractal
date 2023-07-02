import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphractal",
    version="0.4.4",
    author="Jonathan Yik Chang Ting",
    author_email="jonting97@gmail.com",
    description="Package to estimate fractal dimension of 3D surfaces formed from overlapping spheres via box-counting algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jon-Ting/sphractal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research", 
        "License :: OSI Approved :: MIT License"
        "Natural Language :: English", 
        "Operating System :: OS Independent", 
        "Programming Language :: C++", 
        "Programming Language :: Python :: 3", 
        "Topic :: Scientific/Engineering", 
        ]
)

