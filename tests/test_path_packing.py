# coding: utf8
# Copyright: MathDecision

from pytest import raises
from random import random
from time import time

from combinatorial.path_packing import invertir_camino
from combinatorial.path_packing import augmenting_paths
from combinatorial.path_packing import describe_path_packing
from combinatorial.path_packing import menger_path_cut
from combinatorial.path_packing import blocking_collection
from combinatorial.path_packing import reverse_blocking_collection
from combinatorial.path_packing import multiple_augmented_paths
from combinatorial.path_packing import menger_path_cut_speedup
from combinatorial.graph import Grafo

def test_invertir_camino():

    mi_grafo = Grafo([1, 2, 3, 4, 5, 6], [(1, 2), (1, 3), (2, 4), (3, 5), (5, 4), (4, 6) ], directed=True)

    path = [1, 2, 4, 6]

    grafo_path_inv = Grafo([1, 2, 3, 4, 5, 6], [(2, 1), (1, 3), (4, 2), (3, 5), (5, 4), (6, 4) ], directed=True)
    assert invertir_camino(mi_grafo,path) == grafo_path_inv

def test_augmenting_paths():
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7], [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7), (7, 4), (6, 3)], directed=True)

    grafo_final = Grafo([1, 2, 3, 4, 5, 6, 7], [(2, 1), (3, 2), (4, 3), (5, 1), (6, 5), (7, 6), (4, 7), (6, 3)], directed=True)

    B_final = {(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7), (7, 4)}

    assert augmenting_paths(mi_grafo,1,4) == grafo_final, B_final

def test_describe_path_packing():
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7], [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7), (7, 4)], directed=True)
    packing = {[1, 2, 3, 4], [1, 5, 6, 7, 4], [10000]}
    # debería mostrarme error

    assert describe_path_packing(mi_grafo, 1, 4) == packing

def test_menger_path():
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7], [(1, 4), (1, 2), (2, 3), (2,4), (3, 7), (3, 4), (1, 5), (5, 6), (6, 7), (7, 4)], directed=True)
    packing, cut = menger_path_cut(mi_grafo, 1, 4)
    print('este es el packing', packing)
    print('este es el cut', cut)

def test_blocking_collection():
    #mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7], [(1, 2), (1, 3), (3, 5), (3, 4), (5, 6), (4, 6), (4, 7), (1, 2),
                                             #(2, 4)], directed=True)

    mi_grafo =  Grafo([1, 2, 3, 4, 5, 6, 7], [(1, 2), (1,5), (2,3), (2,5), (3,4), (3,5), (3,6), (5,6),(4,6), (4,7),(6,7) ], directed=True)
    blocking = blocking_collection(mi_grafo, 1, 7)
    print('este es blocking', blocking)

def test_reverse_blocking_collection():
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7,8],
                     [(5,8),(6,8),(2,8),(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (3, 5), (3, 6), (5, 6), (4, 6), (4, 7), (6, 7)],
                     directed = True)
    Dprima2, alpha_grafo = reverse_blocking_collection(mi_grafo, 1, 8)
    print('estos son los arcos de Dprima2', Dprima2.aristas)

def test_multiple_augmented_paths():
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7, 8],
                     [(5, 8), (6, 8), (2, 8), (1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (3, 5), (3, 6), (5, 6), (4, 6),
                      (4, 7), (6, 7)],
                     directed=True)
    mi_grafo2 = Grafo([1, 2, 3, 4, 5, 6, 7], [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7), (7, 4), (6, 3)],
                     directed=True)
    D_final,B = multiple_augmented_paths(mi_grafo2, 1, 4)
    print('estos son los arcos de D_final', D_final.aristas)
    print('estas son las aristas de D que están reversadas en D_final', B)

def test_menger_path_cut_speedup():
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7, 8],
                     [(5, 8), (6, 8), (2, 8), (1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (3, 5), (3, 6), (5, 6), (4, 6),
                      (4, 7), (6, 7)],
                     directed=True)
    mi_grafo2 = Grafo([1, 2, 3, 4, 5, 6, 7], [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7), (7, 4), (6, 3)],
                      directed=True)
    packing, cut = menger_path_cut_speedup(mi_grafo2,1,4)
    print('este es el packing', packing)
    print('este es el corte', cut)







