# coding: utf8
# Copyright: MathDecision

from pytest import raises


from ..combinatorial.graph import Grafo
from ..combinatorial.minpath import minimum_cost_from_vertex_v1, minimum_directed_path

def test_minimum_cost_from_vertex_v1():

    n = 30
    vertices = list(range(n))
    aristas = list((i, i + 1) for i in range(n - 1))
    graph = Grafo(vertices, aristas)

    for e in aristas:
        graph.add_info(e, 'costo', 1)

    phi = minimum_cost_from_vertex_v1(graph, 0)
    assert phi == {i: i for i in range(n)}

    n = 30
    vertices = list(range(n))
    aristas = list((i, i + 1) for i in range(n - 1))  + [(0, n - 1)]
    graph = Grafo(vertices, aristas)


    for e in aristas:
        graph.add_info(e, 'costo', 10)
    graph.add_info((0, n - 1), 'costo', 1)

    phi = minimum_cost_from_vertex_v1(graph, 0)
    assert phi == {i: min(10 * i, 1 + 10 * (n - 1 - i)) for i in range(n)}


def test_minimum_directed_path():

    grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)], directed=True)
    assert minimum_directed_path(grafo, 1, 5) == [1, 5]

    grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5)], directed=True)
    assert minimum_directed_path(grafo, 1, 5) == [1, 2, 3, 4, 5]

    grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5)], directed=True)
    assert minimum_directed_path(grafo, 2, 4) == [2, 3, 4]

    with raises(ValueError):
        grafo = Grafo([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5)], directed=True)
        minimum_directed_path(grafo, 4, 1)