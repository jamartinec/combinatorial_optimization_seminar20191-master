# coding: utf8
# Copyright: MathDecision

from pytest import raises
from random import random
from time import time

from combinatorial.caminos import DFS
from combinatorial.caminos import caminos_simples_st_prioritize_minlenFIFO
from combinatorial.graph import Grafo



def test_dfs_iterative():

    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7], [(1, 2), (1, 3), (3, 5), (3, 4), (5, 6), (4, 6), (4, 7), (1, 2),
                                             (2, 4)], directed=True)


    dfs = DFS()
    aristas, padres, P = dfs.do_dfs(tree=mi_grafo, root=1, destino=4)
    print('estas son las aristas', aristas)
    print('estos son los padres', padres)
    print('este es el camino origen destino', P)


def test_caminos_simples_st_prioritize_minlenFIFO():
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7],
                     [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (3, 5), (3, 6), (5, 6), (4, 6), (4, 7), (6, 7)],
                     directed=True)
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6, 7],
                     [(1, 2), (1, 5), (2, 3), (2,6),(2, 5), (3, 4), (3, 5), (3, 6), (5, 6), (4, 6), (4, 7), (6, 7)],
                     directed=True)

    caminos, shortest_caminos, alpha_grafo = caminos_simples_st_prioritize_minlenFIFO(mi_grafo, 1, 6)
    for camino in caminos:
        print(camino.lista_camino())
    for  camino in shortest_caminos:
        print(camino.lista_camino())
    print('este es alpha_grafo',alpha_grafo)


