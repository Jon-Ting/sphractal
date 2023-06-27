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

#include "bcCPU.h"

void seqBC2D(unsigned char* M, const int m, unsigned int* n) {
	unsigned int s = 2;
	unsigned int size = m;
	unsigned char ni = 0; 

	while (size > 2) {
		int sm = s >> 1; // s/2
		unsigned long im;
		unsigned long ismm;

		n[ni] = 0;
		for (unsigned long i = 0; i < (m - 1); i += s) {
			im = i * m;
			ismm = (i + sm) * m;
			for (unsigned long j = 0; j < (m - 1); j += s) {
				M[im + j] = M[(im)+j] || M[(im)+(j + sm)] || M[ismm + j] || M[ismm + (j + sm)];
				n[ni] += M[im + j];
			}
		}
		ni++;
		s <<= 1; // s *= 2;
		size >>= 1; // size /= 2;
	}
}

void seqBC3D(unsigned char* M, const int m, unsigned int* n) {
	unsigned int s = 2;
	unsigned int size = m;
	unsigned char ni = 0;

	while (size > 2) {
		int sm = s >> 1; // s/2
		unsigned long im, kmm;
		unsigned long ismm, ksmmm;

		n[ni] = 0;
		for (unsigned long k = 0; k < (m - 1); k += s) {
			kmm = k * m * m;
			ksmmm = (k + sm) * m * m;
			for (unsigned long i = 0; i < (m - 1); i += s) {
				im = i * m;
				ismm = (i + sm) * m;
				for (unsigned long j = 0; j < (m - 1); j += s) {
					M[kmm + im + j] = M[kmm + im + j]   || M[kmm + im + (j + sm)]   || M[kmm + ismm + j]   || M[kmm + ismm + (j + sm)] ||
						              M[ksmmm + im + j] || M[ksmmm + im + (j + sm)] || M[ksmmm + ismm + j] || M[ksmmm + ismm + (j + sm)];

					n[ni] += M[kmm + im + j];
				}
			}
		}
		ni++;
		s <<= 1; // s *= 2;
		size >>= 1; // size /= 2;
	}
}

void seqBC4D(unsigned char* M, const int m, unsigned int* n) {
	unsigned int s = 2;
	unsigned int size = m;
	unsigned char ni = 0;

	while (size > 2) {
		int sm = s >> 1; // s/2
		unsigned long im, kmm, lmmm;
		unsigned long ismm, ksmmm, lsmmmm;

		n[ni] = 0;
		for (unsigned long l = 0; l < (m - 1); l += s) {
			lmmm = l * m * m * m;
			lsmmmm = (l + sm) * m * m * m;
			for (unsigned long k = 0; k < (m - 1); k += s) {
				kmm = k * m * m;
				ksmmm = (k + sm) * m * m;
				for (unsigned long i = 0; i < (m - 1); i += s) {
					im = i * m;
					ismm = (i + sm) * m;
					for (unsigned long j = 0; j < (m - 1); j += s) {
						M[lmmm + kmm + im + j] = M[lmmm + kmm + im + j]     || M[lmmm + kmm + im + (j + sm)]     || M[lmmm + kmm + ismm + j]     || M[lmmm + kmm + ismm + (j + sm)] ||
										         M[lmmm + ksmmm + im + j]   || M[lmmm + ksmmm + im + (j + sm)]   || M[lmmm + ksmmm + ismm + j]   || M[lmmm + ksmmm + ismm + (j + sm)] ||
										         M[lsmmmm + kmm + im + j]   || M[lsmmmm + kmm + im + (j + sm)]   || M[lsmmmm + kmm + ismm + j]   || M[lsmmmm + kmm + ismm + (j + sm)] ||
										         M[lsmmmm + ksmmm + im + j] || M[lsmmmm + ksmmm + im + (j + sm)] || M[lsmmmm + ksmmm + ismm + j] || M[lsmmmm + ksmmm + ismm + (j + sm)];

						n[ni] += M[lmmm + kmm + im + j];
					}
				}
			}
		}
		ni++;
		s <<= 1; // s *= 2;
		size >>= 1; // size /= 2;
	}
}
