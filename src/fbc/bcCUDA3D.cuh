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

#pragma once

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

// Cuda box-counting algorithm for data in 3D
cudaError_t CudaBC3D(const unsigned char* M, const long long int m, const unsigned char bits_m, const unsigned int TPB, const int nn, unsigned int* n);
