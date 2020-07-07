# coding: utf8
# Copyright: JAMC

#from pytest import raises
from random import random
from time import time

from combinatorial.graph import Grafo
from combinatorial.shortest_paths import Dijkstra
from combinatorial.shortest_paths import Reverse_Dijkstra
from combinatorial.shortest_paths import Bidirectional_Dijkstra
from combinatorial.shortest_paths import SPPTW_basic
from combinatorial.shortest_paths import SPPTW_basic_B
from combinatorial.shortest_paths import spptw_desrochers1988_imp1
from combinatorial.shortest_paths import spptw_desrochers1988_imp2
from combinatorial.shortest_paths import spptw_desrochers1988_imp3

def test_Dijkstra():

    mi_grafo = Grafo([1, 2, 3, 4, 5,6], [(1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,6), (5,4), (5,6)],
                     directed=True)

    l = {(1,2):6, (1,3):4, (2,3):2, (2,4):2, (3,4):1, (3,5):2, (4,6):7, (5,6):3, (5,4):1 }

    d = Dijkstra(mi_grafo,l,1)

def test_Reverse_Dijkstra():

    mi_grafo = Grafo([1, 2, 3, 4, 5,6], [(1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,6), (5,4), (5,6)],
                     directed=True)

    l = {(1,2):6, (1,3):4, (2,3):2, (2,4):2, (3,4):1, (3,5):2, (4,6):7, (5,6):3, (5,4):1 }

    d = Reverse_Dijkstra(mi_grafo,l,6)


def test_Bidirectional_Dijkstra():

    mi_grafo = Grafo([1, 2, 3, 4, 5,6], [(1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,6), (5,4), (5,6)],
                     directed=True)

    l = {(1,2):6, (1,3):4, (2,3):2, (2,4):2, (3,4):1, (3,5):2, (4,6):7, (5,6):3, (5,4):1 }

    d = Bidirectional_Dijkstra(mi_grafo,l,1,6)

def test_SPPTW_basic():

    mi_grafo = Grafo([0,1,2,3,4],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)],directed=True)

    tiempo = {(0,1):8,(0,2):5,(0,3):12,(1,4):4,(2,4):2,(3,4):4}
    costo  = {(0,1):3,(0,2):5,(0,3):2,(1,4):7,(2,4):6,(3,4):3}
    ventana = {0:[0,0],1:[6,14],2:[9,12],3:[8,12],4:[9,15]}
    P = SPPTW_basic(mi_grafo,0,tiempo,costo,ventana)
    print(P)

    return P

def test_SPPTW_basic_B():

    mi_grafo = Grafo([0, 1, 2, 3, 4], [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)], directed=True)

    tiempo = {(0, 1): 8, (0, 2): 5, (0, 3): 12, (1, 4): 4, (2, 4): 2, (3, 4): 4}
    costo = {(0, 1): 3, (0, 2): 5, (0, 3): 2, (1, 4): 7, (2, 4): 6, (3, 4): 3}
    ventana = {0: [0, 0], 1: [6, 14], 2: [9, 12], 3: [8, 12], 4: [9, 15]}
    P = SPPTW_basic_B(mi_grafo, 0, tiempo, costo, ventana)
    print(P)


    return P

def test_spptw_desrochers1988_imp1():

    mi_grafo = Grafo([0, 1, 2, 3, 4], [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)], directed=True)

    tiempo = {(0, 1): 8, (0, 2): 5, (0, 3): 12, (1, 4): 4, (2, 4): 2, (3, 4): 4}
    costo = {(0, 1): 3, (0, 2): 5, (0, 3): 2, (1, 4): 7, (2, 4): 6, (3, 4): 3}
    ventana = {0: [0, 0], 1: [6, 14], 2: [9, 12], 3: [8, 12], 4: [9, 15]}
    P = spptw_desrochers1988_imp1(mi_grafo, 0, tiempo, costo, ventana)
    print(P)
    
    return P

def test_spptw_desrochers1988_imp2():

    mi_grafo = Grafo([0, 1, 2, 3, 4], [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)], directed=True)

    tiempo = {(0, 1): 8, (0, 2): 5, (0, 3): 12, (1, 4): 4, (2, 4): 2, (3, 4): 4}
    costo = {(0, 1): 3, (0, 2): 5, (0, 3): 2, (1, 4): 7, (2, 4): 6, (3, 4): 3}
    ventana = {0: [0, 0], 1: [6, 14], 2: [9, 12], 3: [8, 12], 4: [9, 15]}
    P = spptw_desrochers1988_imp2(mi_grafo, 0, tiempo, costo, ventana)
    print(P)
    return P

def test_spptw_desrochers1988_imp3():

    mi_grafo = Grafo([0, 1, 2, 3, 4], [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)], directed=True)

    tiempo = {(0, 1): 8, (0, 2): 5, (0, 3): 12, (1, 4): 4, (2, 4): 2, (3, 4): 4}
    costo = {(0, 1): 3, (0, 2): 5, (0, 3): 2, (1, 4): 7, (2, 4): 6, (3, 4): 3}
    ventana = {0: [0, 0], 1: [6, 14], 2: [9, 12], 3: [8, 12], 4: [9, 15]}
    P = spptw_desrochers1988_imp3(mi_grafo, 0, tiempo, costo, ventana)
    print(P)
    return P
