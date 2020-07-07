# coding: utf8
# Copyright: MathDecision

from copy import copy

from ..graph import Grafo


def minimum_cost_from_vertex_v1(graph, v):
    """
        El costo de las aristas es positivo.

        S es compacto ssi c(v, w) >= c(v, u) para todo $w \not \in S$, $u \in S$

        $S_1, S_2, .... $ compactos, encajados y $|S_k| = k$.

        En particular,

        $S_1 = {v}$

        $c_S(v, w)$: Costo minimo de v a w a traves de vertices de S.

        $phi_k(w) := c_{S_k}(v, w)$

    """
    n = graph.num_vertices
    S = set()
    phi = {u: float('inf') for u in graph.vertices}
    phi[v] = 0
    while len(S) < n:
        u2add = min(phi.keys() - S, key=lambda _: phi[_])
        S.add(u2add)
        for uvec in graph.vecinos(u2add):
            if uvec not in S:
                phi[uvec] = min(phi[uvec], phi[u2add] + graph.get_info((u2add, uvec), 'costo'))
    return phi



def minimum_directed_path(G, s, t):
    """ Retorna un camino dirigido de s a t de longitud mínima en el grafo G.
    Si no hay tal camino, levanta un ValueError
    :type G: Grafo
    """
    if s == t:
        return [s]
    stack = [s]
    visited = {s}
    ancestors = dict()
    while stack:
        u = stack.pop()
        for v in G.succesors(u):
            if v not in visited:
                if v == t:
                    ancestors[t] = u
                    current = t
                    path = [current]
                    while current in ancestors:
                        current = ancestors[current]
                        path.append(current)
                    return list(reversed(path))
                else:
                    stack.append(v)
                    visited.add(v)
                    ancestors[v] = u
    raise ValueError()

