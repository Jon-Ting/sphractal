#include <pybind11/pybind11.h>
#include <iostream>
#include <cmath>
#include <chrono>
#include <cstring>
#include <fstream>
#include "bcCPU.h"

void pointsTo3DImage(unsigned char* matrix, int* idxarr, int n) {
    for (int i = 0; i < n; i++)
        matrix[idxarr[i]] = 1;
}

int boxCnt3DbinIm(int argc, char* argv[]) {
    // Check command line arguments
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file> <grid_num>\n";
        return 1;
    }

    // Constants
    const int m = std::stoi(argv[1]);
    const int nn = std::log2(m) - 1;

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

    // Allocate memory
    unsigned char* I3d = new unsigned char[m * m * m];
    unsigned int* n3d = new unsigned int[nn];

    // Convert points to 3D binary image
    std::memset(I3d, 0, sizeof(unsigned char) * m * m * m);
    pointsTo3DImage(I3d, idxarr, i);

    // Perform 3D CPU box-counting
    std::fill(n3d, n3d + nn, 0);
    unsigned char* Icpu3d = new unsigned char[m * m * m];
    std::memcpy(Icpu3d, I3d, sizeof(unsigned char) * m * m * m);
    auto start = std::chrono::system_clock::now();
    seqBC3D(Icpu3d, m, n3d);
    auto stop = std::chrono::system_clock::now();
    std::chrono::duration<double> time_cpu = stop - start;

    // Display box-counting results
    // for (int i = 0; i < nn; i++)
    //     std::cout << "    Magnification: " << (2 << i) << " -- Box counts: " << n3d[i] << std::endl;

    // Write output file
    const char* outputFilename = argv[3];
    std::ofstream outfile(outputFilename);
    if (!outfile) {
        std::cerr << "Failed to open file: " << outputFilename << std::endl;
        delete[] Icpu3d, idxarr, I3d, n3d;
        return 1;
    }
    for (int i = 0; i < nn; i++)
        outfile << (2 << i) << " " << n3d[i] << std::endl;

    // Display execution time
    // std::cout << "    3D CPU box-counting duration: " << time_cpu.count() << " seconds" << std::endl;

    // Clean up memory
    delete[] Icpu3d, idxarr, I3d, n3d;
    return 0;
}

PYBIND11_MODULE(runBoxCnt3DbinIm, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("boxCnt3DbinIm", &boxCnt3DbinIm, "A function that adds two numbers");
}
