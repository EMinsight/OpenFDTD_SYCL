# -*- coding: utf-8 -*-
"""
setupPmlHx.py
"""

from numba import jit

@jit(cache=True, nogil=True)#, parallel=True, nopython=True) # prange不可
def setHx(mode, pml_l, Nx, Ny, Nz, iHx, iPmlHx,
    iMin, iMax, jMin, jMax, kMin, kMax, Ni, Nj, Nk, N0):

    lx = pml_l
    ly = pml_l
    lz = pml_l
    imin = iMin - lx + 1
    jmin = jMin - ly + 0
    kmin = kMin - lz + 0
    imax = iMax + lx
    jmax = jMax + ly
    kmax = kMax + lz

    num = 0
    for i in range(imin, imax):
        for j in range(jmin, jmax):
            for k in range(kmin, kmax):
                if (i < 0) or (Nx <  i) or \
                   (j < 0) or (Ny <= j) or \
                   (k < 0) or (Nz <= k):
                    if mode == 1:
                        iPmlHx[num, 0] = i
                        iPmlHx[num, 1] = j
                        iPmlHx[num, 2] = k
                        i_ = max(0, min(Nx,     i))
                        j_ = max(0, min(Ny - 1, j))
                        k_ = max(0, min(Nz - 1, k))
                        n = 0
                        if   i  <  0:
                            n = Ni * (0     ) + Nj * (j_    ) + Nk * (k_    ) + N0
                        elif Nx <  i:
                            n = Ni * (Nx    ) + Nj * (j_    ) + Nk * (k_    ) + N0
                        elif j  <  0:
                            n = Ni * (i_    ) + Nj * (0     ) + Nk * (k_    ) + N0
                        elif Ny <= j:
                            n = Ni * (i_    ) + Nj * (Ny - 1) + Nk * (k_    ) + N0
                        elif k  <  0:
                            n = Ni * (i_    ) + Nj * (j_    ) + Nk * (0     ) + N0
                        elif Nz <= k:
                            n = Ni * (i_    ) + Nj * (j_    ) + Nk * (Nz - 1) + N0
                        iPmlHx[num, 3] = iHx[n]
                    num += 1

    # 配列の大きさ
    if mode == 0:
        return num
