# coding: utf8
# Copyright: MathDecision

from pytest import raises
from random import random
from time import time

from combinatorial.flows import improve_flow
from combinatorial.flows import is_flow
from combinatorial.flows import maximum_flow
from combinatorial.flows import residual_graph
#from combinatorial.flows import _path_directions
from combinatorial.flows import blocking_flow
from combinatorial.flows import augmenting_along_flows
from combinatorial.graph import Grafo

def test_is_flow():

    mi_grafo = Grafo([1, 2, 3, 4], [(1, 2), (1, 3), (2, 3), (3, 4)], directed=True)

    flow = {(1, 2): 3, (1, 3): 2, (2, 3): 1, (3, 4): 5}
    S = set()
    assert not is_flow(flow, mi_grafo, S)

    flow = {(1, 2): 0, (1, 3): 0, (2, 3): 0, (3, 4): 0}
    S = set()
    assert is_flow(flow, mi_grafo, S)

    flow = {(1, 2): 1, (1, 3): 1, (2, 3): 1, (3, 4): 2}
    S = {1, 4}
    assert is_flow(flow, mi_grafo, S)

    flow = {(1, 2): -1, (1, 3): 1, (2, 3): 1, (3, 4): 2}
    S = {1, 4}
    assert not is_flow(flow, mi_grafo, S)


# def test_path_directions():
#     mi_grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (3, 2), (4, 3), (4, 5), (2, 4)],
#                      directed=True)
#     P = [1, 2, 3, 4, 5]
#     phi = {(1, 2): 1, (3, 2): -1, (4, 3): -1, (4, 5): 1}
#     res = _path_directions(mi_grafo, P)
#     assert phi == res

def test_residual_graph():
    mi_grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (3, 2), (4, 3), (4, 5), (2, 4)],
                     directed=True)
    f = {(1, 2): 0, (3, 2): 0, (4, 3): 0, (4, 5): 0, (2, 4): 0}
    cap = {(1, 2): 1, (3, 2): 1, (4, 3): 1, (4, 5): 1, (2, 4): 1}
    residual = residual_graph(f, cap, mi_grafo)
    assert residual.aristas == {(1, 2), (3, 2), (4, 3), (4, 5), (2, 4)}

    mi_grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (3, 2), (4, 3), (4, 5), (2, 4)],
                     directed=True)
    f = {(1, 2): 1, (3, 2): 0.5, (4, 3): 0, (4, 5): 0, (2, 4): 0}
    cap = {(1, 2): 1, (3, 2): 1, (4, 3): 1, (4, 5): 1, (2, 4): 1}
    residual = residual_graph(f, cap, mi_grafo)
    assert residual.aristas == {(2, 1), (3, 2), (2, 3), (4, 3), (4, 5), (2, 4)}

    mi_grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (3, 2), (4, 3), (4, 5), (2, 4)],
                     directed=True)
    f = {(1, 2): 0.1, (3, 2): 0.5, (4, 3): 0.5, (4, 5): 0.5, (2, 4): 0.5}
    cap = {(1, 2): 1, (3, 2): 1, (4, 3): 1, (4, 5): 1, (2, 4): 1}
    residual = residual_graph(f, cap, mi_grafo)
    assert residual.aristas == {(1, 2), (2, 1), (3, 2), (2, 3), (4, 3), (3, 4),
                                (4, 5), (5, 4), (2, 4), (4, 2)}


def test_improve_flows():
    mi_grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (3, 2), (4, 3), (4, 5), (2, 4)],
                     directed=True)
    cap = {(1, 2): 1, (3, 2): 1, (4, 3): 1, (4, 5): 1, (2, 4): 1}
    f = {(1, 2): 0, (3, 2): 0, (4, 3): 0, (4, 5): 0, (2, 4): 0}
    P = [1, 2, 4, 5]
    assert is_flow(f, mi_grafo, {1, 5}, cap=cap)
    ff, epsilon = improve_flow(f, cap, mi_grafo, P)
    assert is_flow(ff, mi_grafo, {1, 5}, cap=cap)
    assert epsilon == 1
    assert ff[(1, 2)] == 1
    assert ff[(2, 4)] == 1
    assert ff[(4, 5)] == 1

    mi_grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (3, 2), (4, 3), (4, 5), (2, 4)],
                     directed=True)
    cap = {(1, 2): 1, (3, 2): 1, (4, 3): 1, (4, 5): 1, (2, 4): 1}
    f = {(1, 2): 0.5, (3, 2): 0, (4, 3): 0, (4, 5): 0.5, (2, 4): 0.5}
    assert is_flow(f, mi_grafo, {1, 5}, cap=cap)
    # (1, 2), (2, 1), (3, 2), (4, 3), (4, 5), (5, 4), (2, 4), (4, 2)
    P = [1, 2, 4, 5]
    ff, epsilon = improve_flow(f, cap, mi_grafo, P)
    assert is_flow(ff, mi_grafo, {1, 5}, cap=cap)
    assert epsilon == 0.5
    assert ff[(1, 2)] == 1
    assert ff[(2, 4)] == 1
    assert ff[(4, 5)] == 1


def test_maximum_flows():
    mi_grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (3, 2), (4, 3), (4, 5), (2, 4)],
                     directed=True)
    cap = {(1, 2): 1, (3, 2): 1, (4, 3): 1, (4, 5): 1, (2, 4): 1}
    f = {(1, 2): 1, (3, 2): 0, (4, 3): 0, (4, 5): 1, (2, 4): 1}
    P = [1, 2, 4, 5]
    assert is_flow(f, mi_grafo, {1, 5}, cap=cap)
    ff = maximum_flow(mi_grafo, cap, 1, 5)
    assert is_flow(ff, mi_grafo, {1, 5}, cap=cap)
    assert ff == f

    mi_grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (2, 3), (2, 4), (4, 5), (3, 5)],
                    directed=True)
    cap = {(1, 2): 4, (2, 3): 2, (2, 4): 1, (4, 5): 2, (3, 5): 1}
    f = {(1, 2): 2, (2, 3): 1, (2, 4): 1, (4, 5): 1, (3, 5): 1}
    assert is_flow(f, mi_grafo, {1, 5}, cap=cap)
    ff = maximum_flow(mi_grafo, cap, 1, 5)
    assert is_flow(ff, mi_grafo, {1, 5}, cap=cap)
    assert ff == f

    N = 10000
    vertices = ['s', 't'] + ['p{}'.format(k) for k in range(1, N + 1)] + ['q{}'.format(k) for k in range(1, N + 1)]
    mi_grafo = Grafo(vertices, [('s', 'p1'), ('s', 'q1')]  \
                     + [('p{}'.format(k), 'p{}'.format(k + 1)) for k in range(1, N)] \
                     + [('q{}'.format(k), 'q{}'.format(k + 1)) for k in range(1, N)] \
                     + [('p{}'.format(N), 't'), ('q{}'.format(N), 't')],
                     directed=True)
    cap = {e: 1 for e in mi_grafo.aristas}
    f = {e: 1 for e in mi_grafo.aristas}
    assert is_flow(f, mi_grafo, {'s', 't'}, cap=cap)
    ff = maximum_flow(mi_grafo, cap, 's', 't')
    assert is_flow(ff, mi_grafo, {'s', 't'}, cap=cap)
    assert ff == f

    N = 10000
    start = time()
    vertices = ['s', 't'] + ['p{}'.format(k) for k in range(1, N + 1)] + ['q{}'.format(k) for k in range(1, N + 1)]
    mi_grafo = Grafo(vertices, [('s', 'p1'), ('s', 'q1')]  \
                     + [('p{}'.format(k), 'p{}'.format(k + 1)) for k in range(1, N)] \
                     + [('q{}'.format(k), 'q{}'.format(k + 1)) for k in range(1, N)] \
                     + [('p{}'.format(N), 't'), ('q{}'.format(N), 't')],
                     directed=True)
    cap = {e: random() for e in mi_grafo.aristas}
    ff = maximum_flow(mi_grafo, cap, 's', 't')
    assert is_flow(ff, mi_grafo, {'s', 't'}, cap=cap)
    delta = (time() - start)
    assert delta < 1.0


def test_blocking_flow():
    mi_grafo = Grafo([1, 2, 3, 4, 5, 6], [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6), (2, 3), (4, 5)],
                     directed=True)
    cap = {(1, 2): 3, (1, 3): 3, (2, 4): 3, (3, 5): 2, (4, 6): 2, (5, 6): 3, (2, 3): 2, (4, 5): 4}

    blocking_f= blocking_flow(mi_grafo, 1, 6, cap)
    print('este es blocking_f',blocking_f)


def test_augmenting_along_flows():
    mi_grafo = Grafo([1, 2, 3, 4, 5,6], [(1,2), (1,3), (2,4), (3,5), (4,6), (5,6), (2,3), (4,5)],
                     directed=True)

    cap = {(1,2):3, (1,3):3, (2,4):3, (3,5):2, (4,6):2, (5,6):3, (2,3):2, (4,5):4}

    mi_grafo2 =Grafo([1, 2, 3, 4, 5, 6], [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6), (2, 3), (5,4)],
          directed=True)

    mi_grafo3 = Grafo([0, 1, 2, 3, 4, 5], [(0,1),(0,2),(1, 2), (1, 3), (1,4), (2,4),(4,3),(4,5),(3,5)],
                      directed=True)

    cap2 = {(1,2):10, (1,3):8, (2,4):5, (3,5):10, (4,6):7, (5,6):10, (2,3):2, (5,4):8}

    cap3 ={(0,1):10,(0,2):10,(1, 2):2,(1, 3):4,(1,4):8,(2,4):9,(4,3):6,(4,5):10,(3,5):10}


    flow1 = {(1,2):0, (1,3):0, (2,4):0, (3,5):0, (4,6):0, (5,6):0, (2,3):0, (4,5):0}

    flow2 = {(1, 2): 0, (1, 3): 0, (2, 4): 0, (3, 5): 0, (4, 6): 0, (5, 6): 0, (2, 3): 0, (5,4): 0}

    flow3 = {(0,1):0,(0,2):0,(1, 2):0,(1, 3):0,(1,4):0,(2,4):0,(4,3):0,(4,5):0,(3,5):0}

    f = augmenting_along_flows(mi_grafo3, flow3, cap3, 0, 5)



