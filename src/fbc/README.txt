Fast Box-Counting Algorithm
Juan Ruiz de Miras and Miguel Ángel Posadas. University of Granada - SPAIN. 2022.
Last update: october - 2022

The box-counting (BC) algorithm is one of the most popular methods for calculating the fractal dimension (FD) of binary data. 
However, high computation times are needed to calculate the BC of large datasets composed of data in 2D, 3D or 4D.
Here, we provide the source code of a very efficient parallel implementation of the BC algorithm for its execution on Graphics Processing Units (GPU).

The file fbc.zip contains:
  - bcCUDA2D.cu and bcCUDA2D.cuh: CUDA/C++ files with the implementation on GPU of the box-counting algorithm for binary 2D data
  - bcCUDA3D.cu and bcCUDA3D.cuh: CUDA/C++ files with the implementation on GPU of the box-counting algorithm for binary 3D data
  - bcCUDA4D.cu and bcCUDA4D.cuh: CUDA/C++ files with the implementation on GPU of the box-counting algorithm for binary 4D data
  - bcCPU.cpp and bcCPU.h: C++ files with the implementation on CPU of the box-counting algorithm for binary 2D, 3D and 4D data
  - test.cpp: example of C++ main file executing the GPU box-counting algorithms
  - license.html: terms of the license for the source code of Fast Box-counting
  - README.txt: this file

1. REQUERIMENTS for compilation and execution

Hardware: Computer with a capable CUDA GPU (https://developer.nvidia.com/cuda-gpus)
Software: 
  - CUDA SDK Toolkit (https://developer.nvidia.com/cuda-toolkit)
  - C++ compiler (the binaries folder must be included in the enviroment variable PATH of the OS)

2. COMPILATION
 
The test.cpp file can be compiled with the following command: > nvcc -O3 -o test bcCUDA4D.cu bcCUDA3D.cu bcCUDA2D.cu bcCPU.cpp test.cpp

3. CITATION

If Fast Box-Counting has been useful for your research, please, cite as:
"Fast Computation of Fractal Dimension for 2D, 3D and 4D Data" 
Juan Ruiz de Miras, Miguel Ángel Posadas, Antonio José Ibáñez-Molina, María Felipa Soriano and Sergio Iglesias-Parro
2022

4. CONTACT AND SUGGESTIONS

For contact information: http://www.ugr.es/~demiras/"
