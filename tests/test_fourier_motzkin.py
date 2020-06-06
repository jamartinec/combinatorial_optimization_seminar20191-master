from time import time

from combinatorial.fourier_motzkin import f_m
import numpy as np

def test_f_m():
    #a = np.array([[-1, 0, 0, -1], [0, -1, 0, -1], [0, 0, -1, -1], [-1, -1, 0, -3], [-1, 0, -1, -3], [0, -1, -1, -3],[1, 1, 1, 6]], dtype=np.float64)

    a = np.array([[1,-5,2,7],[3,-2,-6,-12],[-2,5,-4,-10],[-3,6,-3,-9],[0,-10,1,-15]], dtype=np.float64)

    dicci = f_m(a)
    print(dicci)
