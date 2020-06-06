# coding: utf8
# Copyright: MathDecision

from pytest import raises

from ..combinatorial.eulpath import eulerian_path
from ..combinatorial.eulpath import get_naive_semieulerian_path
from ..combinatorial.eulpath import get_naive_semieulerian_path_and_stack
from ..combinatorial.eulpath import get_naive_semieulerian_path_enriched
from ..combinatorial.eulpath import verify_flow_condition
from ..combinatorial.graph import Grafo


def test_verify_flow_condition():

    graph = Grafo([1, 2], [(1, 2)])

    with raises(AssertionError):
        verify_flow_condition(graph, 1, 2)

    graph = Grafo([1, 2], [(1, 2)], directed=True)

    assert verify_flow_condition(graph, 1, 2)

    assert not verify_flow_condition(graph, 2, 1)

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], directed=True)

    assert verify_flow_condition(graph, 1, 4)

    assert not verify_flow_condition(graph, 4, 1)

    assert not verify_flow_condition(graph, 2, 1)

    assert not verify_flow_condition(graph, 2, 4)


def test_get_naive_semieulerian_path():


    graph = Grafo([1, 2], [(1, 2)], directed=True)
    assert get_naive_semieulerian_path(graph, 1, 2) == [1, 2]

    graph = Grafo([1, 2], [(1, 2)], directed=True)
    assert get_naive_semieulerian_path(graph, 2, 1) == [2]

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], directed=True)
    assert get_naive_semieulerian_path(graph, 1, 4) == [1, 2, 3, 4]

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4)], directed=True)
    assert get_naive_semieulerian_path(graph, 1, 4) == [1, 2, 3, 4]

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4)], directed=True)
    assert get_naive_semieulerian_path(graph, 3, 4) == [3, 4]

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4), (4, 1)], directed=True)
    assert get_naive_semieulerian_path(graph, 1, 1) == [1, 2, 3, 4, 1]

def test_get_naive_semieulerian_path_and_stack():


    stack = []
    graph = Grafo([1, 2], [(1, 2)], directed=True)
    assert get_naive_semieulerian_path_and_stack(graph, 1, 2, stack) == [1, 2]
    assert stack == []

    stack = []
    graph = Grafo([1, 2], [(1, 2)], directed=True)
    assert get_naive_semieulerian_path_and_stack(graph, 2, 1, stack) == [2]
    assert stack == []

    stack = []
    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], directed=True)
    assert get_naive_semieulerian_path_and_stack(graph, 1, 4, stack) == [1, 2, 3, 4]
    assert stack == []

    stack = []
    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4)], directed=True)
    assert get_naive_semieulerian_path_and_stack(graph, 1, 4, stack) == [1, 2, 3, 4]
    assert stack == [2]

    stack = []
    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4)], directed=True)
    assert get_naive_semieulerian_path_and_stack(graph, 3, 4, stack) == [3, 4]
    assert stack == []

    stack = []
    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4), (4, 1)], directed=True)
    assert get_naive_semieulerian_path_and_stack(graph, 1, 1, stack) == [1, 2, 3, 4, 1]
    assert stack == [2]


def test_get_naive_semieulerian_path_enriched():

    graph = Grafo([1, 2], [(1, 2)], directed=True)
    esq, sc, ev = get_naive_semieulerian_path_enriched(graph, 1, 2)
    assert esq.name == 1
    sucs = esq.get_succesors()
    assert len(sucs) == 1
    suc = list(sucs)[0]
    assert suc.name == 2
    assert len(suc.get_succesors()) == 0
    assert sc == {1: 0, 2: 0}
    assert ev == set()

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], directed=True)
    esq, sc, ev = get_naive_semieulerian_path_enriched(graph, 1, 4)
    assert sc == {1: 0, 2: 0, 3: 0, 4: 0}
    assert ev == set()

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4)], directed=True)
    esq, sc, ev = get_naive_semieulerian_path_enriched(graph, 1, 4)
    assert sc == {1: 0, 2: 1, 3: 0, 4: 0}
    assert ev == {2}


    #
    # graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4)], directed=True)
    # assert get_naive_semieulerian_path(graph, 3, 4) == [3, 4]


def test_eulerian_path():


    graph = Grafo([1, 2], [(1, 2)], directed=True)
    assert eulerian_path(graph, 1, 2) == [1, 2]

    graph = Grafo([1, 2], [(1, 2)], directed=True)
    with raises(AssertionError):
        eulerian_path(graph, 2, 1)

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], directed=True)
    assert eulerian_path(graph, 1, 4) == [1, 2, 3, 4]

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4)], directed=True)
    with raises(AssertionError):
        eulerian_path(graph, 1, 4)

    stack = []
    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4)], directed=True)
    assert eulerian_path(graph, 3, 4) == [3, 4]

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (2, 4), (3, 4), (4, 1)], directed=True)
    with raises(AssertionError):
        eulerian_path(graph, 1, 1)

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1)], directed=True)
    assert eulerian_path(graph, 1, 1) == [1, 2, 3, 4]

    graph = Grafo(['s', 1, 2, 3, 't', 4, 5], [('s', 1), (1, 2), (2, 3), (3, 't'), (1, 4), (4, 3), (3, 5), (5, 1)], directed=True)
    assert eulerian_path(graph, 's', 't') == ['s', 1, 2, 3, 5, 1, 4, 3, 't']
