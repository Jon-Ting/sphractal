#include <iostream>
#include <cmath>
#include <chrono>
#include <cstring>
#include <fstream>
#include "bcCUDA3D.cuh"

// Function to convert points to a 3D binary image
void pointsTo3DImage(unsigned char* matrix, int* idxarr, int n) {
    for (int i = 0; i < n; i++)
        matrix[idxarr[i]] = 1;
}

int main(int argc, char* argv[]) {
    // Check command line arguments
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file> <grid_num>\n";
        return 1;
    }

    // Constants
    const int m = std::stoi(argv[1]);
    const int nn = std::log2(m) - 1;
    const unsigned char bits_m = nn + 1; // 2^bits_m = m

    // Read input file
    const char* filename = argv[2];
    int* idxarr = new int[m * m * m];
    std::ifstream infile(filename);
    if (!infile) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        delete[] idxarr;
        return 1;
    }
    int n, i = 0;
    while (infile >> n)
        idxarr[i++] = n;

    // Allocate memory and set threads per block
    unsigned char* I3d = nullptr;
    unsigned int* n3d = nullptr;
    const unsigned int TPB = 128;

    // Check CUDA status for memory allocation
    cudaError_t cudaStatus;
    cudaStatus = cudaMallocHost((void**)&I3d, sizeof(unsigned char) * m * m * m);
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(cudaStatus));
        delete[] idxarr;
        return 1;
    }
    cudaStatus = cudaMallocHost((void**)&n3d, sizeof(unsigned int) * nn);
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(cudaStatus));
        cudaFreeHost(I3d);
        delete[] idxarr;
        return 1;
    }

    // Convert points to 3D binary image
    std::memset(I3d, 0, sizeof(unsigned char) * m * m * m);
    pointsTo3DImage(I3d, idxarr, i);

    // Perform 3D GPU box-counting
    for (int i = 0; i < nn; i++)
        n3d[i] = 0;
    auto start = std::chrono::system_clock::now();
    cudaStatus = CudaBC3D(I3d, m, bits_m, TPB, nn, n3d);
    auto stop = std::chrono::system_clock::now();
    std::chrono::duration<double> time_gpu = stop - start;
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "CudaBC3D failed!");
        cudaFreeHost(I3d);
        delete[] idxarr;
        cudaFreeHost(n3d);
        return 1;
    }

    // Display box-counting results
    // for (int i = 0; i < nn; i++)
    //     std::cout << "    Magnification: " << (2 << i) << " -- Box counts: " << n3d[i] << std::endl;

    // Write output file
    const char* outputFilename = argv[3];
    std::ofstream outfile(outputFilename);
    if (!outfile) {
        std::cerr << "Failed to open file: " << outputFilename << std::endl;
        cudaFreeHost(I3d);
        delete[] idxarr;
        cudaFreeHost(n3d);
        return 1;
    }

    // Display execution time
    // std::cout << "    3D GPU box-counting duration: " << time_gpu.count() << " seconds" << std::endl;

    // Clean up memory
    cudaFreeHost(I3d);
    delete[] idxarr;
    cudaFreeHost(n3d);

    return 0;
}

