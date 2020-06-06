# coding: utf8
# Copyright: MathDecision

from pytest import raises
from random import random
from time import time

from combinatorial.knapsack_problem import kp_recursive
from combinatorial.knapsack_problem import kp_dynamicp


def test_kp_recursive():
    p = [6,5,8,9,6,7,3]
    w = [2,3,6,7,5,9,4]
    d=9
    n=7

    valor = kp_recursive(d , w , p , n)
    print('este es el valor óptimo', valor)

def test_kp_dynamicp():
    p = [6, 5, 8, 9, 6, 7, 3]
    w = [2, 3, 6, 7, 5, 9, 4]
    d = 9
    n = 7

    valor = kp_dynamicp(d, w, p, n)
    print('este es el valor óptimo',valor)
