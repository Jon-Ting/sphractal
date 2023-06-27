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

#include <iostream>
#include <iomanip>
#include <stdio.h>

#include "bcCUDA2D.cuh"

__global__ void BCKernel2D(unsigned char* M, const long long int m, const unsigned long long int bits_m, const unsigned long long int sm,
						   const unsigned long long bits_s, const unsigned long long bits_TPB, unsigned int* n)
{
	register unsigned long long int tid = threadIdx.x; 
	register unsigned long long int idx = (blockIdx.x << bits_TPB) + tid; // 2 ^ bits_TPB = TPB

	// identifies grid index (i, j) from block and thread values
	register unsigned long long int i = idx >> (bits_m - bits_s); // i index: idx / (m/s)
	register unsigned long long int j = idx & ((m >> bits_s) - 1); // j index: idx mod (m/s)

	// global location of position (0, 0) of the grid (i, j) is gi + gj
	const register unsigned long long int gi = (i << bits_s) << bits_m;  
	const register unsigned long long int gism = ((i << bits_s) + sm) << bits_m;  
	const register unsigned long long int gj = j << bits_s;  
	const register unsigned long long int gjsm = (j << bits_s) +sm;  

	// compute and store the occupancy value of the grid (i, j)
	M[gi + gj] = M[gi + gj] || M[gi + gjsm] || M[gism + gj] || M[gism + gjsm];
	atomicAdd(n, M[gi + gj]);
}

cudaError_t CudaBC2D(const unsigned char* M, const long long int m, const unsigned char bits_m, const unsigned int TPB, const int nn, unsigned int* n)
{
    cudaError_t cudaStatus;

    // Choose which GPU to run on, change this on a multi-GPU system.
    cudaStatus = cudaSetDevice(0);
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaSetDevice failed!  Do you have a CUDA-capable GPU installed?");
		return cudaStatus;
    }

	// CPU-GPU data transfers
	unsigned char* device_M = 0; // matrix M in GPU device
	unsigned int* device_n = 0; // array n in GPU device
	cudaStatus = cudaMalloc((void**)&device_M, m * m * sizeof(unsigned char));
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaMalloc failed!");
		return cudaStatus;
	}
    cudaStatus = cudaMalloc((void**)&device_n, nn * sizeof(unsigned int));
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaMalloc failed!");
		cudaFree(device_M);
		return cudaStatus;
	}
	cudaStatus = cudaMemcpy(device_M, M, m * m * sizeof(unsigned char), cudaMemcpyHostToDevice);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "cudaMemcpy failed!");
		cudaFree(device_M);
		cudaFree(device_n);
		return cudaStatus;
	}
	cudaStatus = cudaMemset(device_n, 0, nn * sizeof(unsigned int));
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "cudaMemcpy failed!");
		cudaFree(device_M);
		cudaFree(device_n);
		return cudaStatus;
	}

	dim3 grid, block(TPB, 1); // variables for kernel launching
	unsigned int s = 2;
	unsigned int size = m;
	unsigned char ni = 0;
	unsigned char bits_TPB = log(TPB)/log(2); // 2^bits_TPB = TPB

	while (size > 2) {
		unsigned int sm = s >> 1; // sm = s/2
		unsigned long long int num_box = (m*m) / (s*s);
			
		if (num_box >= TPB) {
			grid.x = ceilf(num_box / (float)TPB); // m/s *m/s = (grid_size * TPB)
			grid.y = 1;
		} else {
			grid.x = 1; grid.y = 1;
			block.x = num_box; block.y = 1;
			bits_TPB = log(num_box)/log(2);
		}

		// BCKernel call. Compute box-counting for grids of size s x s
		BCKernel2D<<<grid, block>>>(device_M, m, bits_m, sm, ni + 1, bits_TPB, &device_n[ni]);

		ni++;
		s <<= 1;
		size >>= 1;
	}
	//cudaDeviceSynchronize();

	// GPU-CPU data transfer of the box-counting results
	cudaStatus = cudaMemcpy(n, device_n, nn * sizeof(unsigned int), cudaMemcpyDeviceToHost);

	cudaFree(device_M);
	cudaFree(device_n);
	return cudaStatus;
}

