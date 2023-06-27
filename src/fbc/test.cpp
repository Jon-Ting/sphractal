//===============================================================================
// This file is part of the software Fast Box-Counting:
// https://www.ugr.es/~demiras/fbc
//
// Copyright(c)2022 University of Granada - SPAIN
//
// FOR RESEARCH PURPOSES ONLY.THE SOFTWARE IS PROVIDED "AS IS," AND THE
// UNIVERSITY OF GRANADA DO NOT MAKE ANY WARRANTY, EXPRESS OR IMPLIED, INCLUDING
// BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
// PURPOSE, NOR DO THEY ASSUME ANY LIABILITY OR RESPONSIBILITY FOR THE USE
// OF THIS SOFTWARE.
//
// For more information see license.html
// ===============================================================================
//
// Authors: Juan Ruiz de Miras and Miguel Ángel Posadas, 2022
// Contact: demiras@ugr.es

// compile: nvcc -O3 -o test bcCUDA4D.cu bcCUDA3D.cu bcCUDA2D.cu bcCPU.cpp test.cpp

#include <iostream>
#include <iomanip>
#include <stdio.h>
#include <vector>
#include <cmath>
#include <chrono>
#include <cstring> 

#include "bcCUDA2D.cuh"
#include "bcCUDA3D.cuh"
#include "bcCUDA4D.cuh"
#include "bcCPU.h"

void random2DImage(long long int size, unsigned char* matrix, unsigned int ones_percent)
{
	srand(10); //seed for reproduction
	for (auto i = 0; i < size; i++)
		for (auto j = 0; j < size; j++) 
			if ((rand() % 100) < ones_percent) matrix[i + j * size] = 1;
			else matrix[i + j * size] = 0;
}

void random3DImage(long long int size, unsigned char* matrix, unsigned int ones_percent)
{
	srand(10); //seed for reproduction
	for (auto i = 0; i < size; i++)
		for (auto j = 0; j < size; j++)
			for (auto k = 0; k < size; k++)
				if ((rand() % 100) < ones_percent) matrix[i + j * size + k * size * size] = 1;
				else matrix[i + j * size + k * size * size] = 0;
}

void random4DImage(long long int size, unsigned char* matrix, unsigned int ones_percent)
{
	srand(10); //seed for reproduction
	for (auto i = 0; i < size; i++)
		for (auto j = 0; j < size; j++)
			for (auto k = 0; k < size; k++)
				for (auto l = 0; l < size; l++)
					if ((rand() % 100) < ones_percent) matrix[i + j * size + k * size * size + l * size * size * size] = 1;
					else matrix[i + j * size + k * size * size + l * size * size * size] = 0;
}

int main()
{
	long long int m;
	cudaError_t cudaStatus;
	std::chrono::time_point<std::chrono::system_clock> start, stop;

	std::vector<long long int> sizes2D = {128,1024,4096,8192,16384,32768,65536}; // size of 65536 requires a GPU with 4GB of global memory

	//////////////////////////////
	// 2D TEST
	//////////////////////////////																 
	// SELECT THE SIZE OF THE 2D IMAGE TO PROCESS
	m = sizes2D.at(4);

	// SELECT THE PERCENTAGE OF 1's IN THE IMAGE (value from 0 to 100)
	unsigned int ones_percent = 20;

	// SELECT THE SIZE OF TPB (threads per block)
	unsigned int TPB = 128;
	
	int nn = log(m) / log(2) - 1;
	unsigned char bits_m = nn + 1; // 2^bits_m = m

	unsigned char* I2d;
	unsigned int* n2d;
	cudaStatus = cudaMallocHost((void**)&I2d, sizeof(unsigned char) * m * m);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(cudaStatus));
		return 1;
	}
	cudaStatus = cudaMallocHost((void**)&n2d, sizeof(unsigned int) * nn);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(cudaStatus));
		return 1;
	}

	std::cout << "******************************" << std::endl;
	std::cout << "2D	 TEST" << std::endl;
	std::cout << "******************************" << std::endl;
	std::cout << "Generating random image of size " << m << "x" << m << " with " << ones_percent << "% of 1's" << std::endl;
	random2DImage(m, I2d, ones_percent);

	//////////////////////
	// box-counting 2D CPU
	//////////////////////
	std::cout << "Computing CPU box-counting algorithm" << std::endl;
	for (int i = 0; i < nn; i++) n2d[i] = 0;
	unsigned char* Icpu2d = new unsigned char[m * m];
	memcpy(Icpu2d, I2d, sizeof(unsigned char) * m * m);
	start = std::chrono::system_clock::now();
	seqBC2D(Icpu2d, m, n2d);
	stop = std::chrono::system_clock::now();
	std::chrono::duration<double> time_cpu = stop - start;
	// show box-counting results
	for (int i = 0; i < nn; i++) {
		std::cout << "s: " << (2 << i) << " -- n: " << n2d[i] << std::endl;
	}
	std::cout << "Time CPU box-counting: " << time_cpu.count() << " seconds" << std::endl;

	//////////////////////
	// box-counting 2D GPU
	//////////////////////
	std::cout << "Computing GPU box-counting algorithm" << std::endl;
	for (int i = 0; i < nn; i++) n2d[i] = 0;
	start = std::chrono::system_clock::now();
	cudaStatus = CudaBC2D(I2d, m, bits_m, TPB, nn, n2d);
	stop = std::chrono::system_clock::now();
	std::chrono::duration<double> time_gpu = stop - start;
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CudaBC2D failed!");
		return 1;
	}
	// show box-counting results
	for (int i = 0; i < nn; i++) {
		std::cout << "s: " << (2 << i) << " -- n: " << n2d[i] << std::endl;
	}
	std::cout << "Time GPU box-counting: " << time_gpu.count() << " seconds" << std::endl;

	cudaFreeHost(I2d);
	delete Icpu2d;
	cudaFreeHost(n2d);


	//////////////////////////////
	// 3D TEST
	//////////////////////////////																 
	std::vector<long long int> sizes3D = { 64,128,256,512,1024,2048 }; // size of 2048 requires a GPU with 8GB of global memory

	// SELECT THE SIZE OF THE 3D IMAGE TO PROCESS
	m = sizes3D.at(3);

	// SELECT THE SIZE OF TPB (threads per block)
	TPB = 128;
	
	nn = log(m) / log(2) - 1;
	bits_m = nn + 1; // 2^bits_m = m

	unsigned char* I3d;
	unsigned int* n3d;
	cudaStatus = cudaMallocHost((void**)&I3d, sizeof(unsigned char) * m * m * m);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(cudaStatus));
		return 1;
	}
	cudaStatus = cudaMallocHost((void**)&n3d, sizeof(unsigned int) * nn);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(cudaStatus));
		return 1;
	}

	std::cout << "******************************" << std::endl;
	std::cout << "3D	 TEST" << std::endl;
	std::cout << "******************************" << std::endl;
	std::cout << "Generating random image of size " << m << "x" << m << "x" << m << " with " << ones_percent << "% of 1's" << std::endl;
	random3DImage(m, I3d, ones_percent);

	//////////////////////
	// box-counting 3D CPU
	//////////////////////
	std::cout << "Computing CPU box-counting algorithm" << std::endl;
	for (int i = 0; i < nn; i++) n3d[i] = 0;
	unsigned char* Icpu3d = new unsigned char[m * m * m];
	memcpy(Icpu3d, I3d, sizeof(unsigned char) * m * m * m);
	start = std::chrono::system_clock::now();
	seqBC3D(Icpu3d, m, n3d);
	stop = std::chrono::system_clock::now();
	time_cpu = stop - start;
	// show box-counting results
	for (int i = 0; i < nn; i++) {
		std::cout << "s: " << (2 << i) << " -- n: " << n3d[i] << std::endl;
	}
	std::cout << "Time CPU box-counting: " << time_cpu.count() << " seconds" << std::endl;

	//////////////////////
	// box-counting 3D GPU
	//////////////////////
	std::cout << "Computing GPU box-counting algorithm" << std::endl;
	for (int i = 0; i < nn; i++) n3d[i] = 0;
	start = std::chrono::system_clock::now();
	cudaStatus = CudaBC3D(I3d, m, bits_m, TPB, nn, n3d);
	stop = std::chrono::system_clock::now();
	time_gpu = stop - start;
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CudaBC2D failed!");
		return 1;
	}
	// show box-counting results
	for (int i = 0; i < nn; i++) {
		std::cout << "s: " << (2 << i) << " -- n: " << n3d[i] << std::endl;
	}
	std::cout << "Time GPU box-counting: " << time_gpu.count() << " seconds" << std::endl;

	cudaFreeHost(I3d);
	delete Icpu3d;
	cudaFreeHost(n3d);


	//////////////////////////////
	// 4D TEST
	//////////////////////////////																 
	std::vector<long long int> sizes4D = { 32,64,128,256 }; // size of 256 requires a GPU with 4GB of global memory

	// SELECT THE SIZE OF THE 4D IMAGE TO PROCESS
	m = sizes4D.at(2);

	// SELECT THE SIZE OF TPB (threads per block)
	TPB = 128;

	nn = log(m) / log(2) - 1;
	bits_m = nn + 1; // 2^bits_m = m

	unsigned char* I4d;
	unsigned int* n4d;
	cudaStatus = cudaMallocHost((void**)&I4d, sizeof(unsigned char) * m * m * m * m);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(cudaStatus));
		return 1;
	}
	cudaStatus = cudaMallocHost((void**)&n4d, sizeof(unsigned int) * nn);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(cudaStatus));
		return 1;
	}

	std::cout << "******************************" << std::endl;
	std::cout << "4D	 TEST" << std::endl;
	std::cout << "******************************" << std::endl;
	std::cout << "Generating random image of size " << m << "x" << m << "x" << m << "x" << m << " with " << ones_percent << "% of 1's" << std::endl;
	random4DImage(m, I4d, ones_percent);

	//////////////////////
	// box-counting 4D CPU
	//////////////////////
	std::cout << "Computing CPU box-counting algorithm" << std::endl;
	for (int i = 0; i < nn; i++) n4d[i] = 0;
	unsigned char* Icpu4d = new unsigned char[m * m * m * m];
	memcpy(Icpu4d, I4d, sizeof(unsigned char) * m * m * m * m);
	start = std::chrono::system_clock::now();
	seqBC4D(Icpu4d, m, n4d);
	stop = std::chrono::system_clock::now();
	time_cpu = stop - start;
	// show box-counting results
	for (int i = 0; i < nn; i++) {
		std::cout << "s: " << (2 << i) << " -- n: " << n4d[i] << std::endl;
	}
	std::cout << "Time CPU box-counting: " << time_cpu.count() << " seconds" << std::endl;

	//////////////////////
	// box-counting 4D GPU
	//////////////////////
	std::cout << "Computing GPU box-counting algorithm" << std::endl;
	for (int i = 0; i < nn; i++) n4d[i] = 0;
	start = std::chrono::system_clock::now();
	cudaStatus = CudaBC4D(I4d, m, bits_m, TPB, nn, n4d);
	stop = std::chrono::system_clock::now();
	time_gpu = stop - start;
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "CudaBC2D failed!");
		return 1;
	}
	// show box-counting results
	for (int i = 0; i < nn; i++) {
		std::cout << "s: " << (2 << i) << " -- n: " << n4d[i] << std::endl;
	}
	std::cout << "Time GPU box-counting: " << time_gpu.count() << " seconds" << std::endl;
	std::cout << "********************************************************************************" << std::endl;

	cudaFreeHost(I4d);
	delete Icpu4d;
	cudaFreeHost(n4d);

	return 0;
}
