# coding: utf8
# Copyright: MathDecision


"""
Sea D=(V,A) un digrafo, y s,t en V. Un path packing es una colección de s-t caminos arco disjuntos
de tamaño máximo.

"""

from ..graph import Grafo
from ..minpath import minimum_directed_path
from ..utils import inv
from ..eulpath import get_naive_semieulerian_path
from ..caminos import caminos_simples_prioritize_minlength_fifo_reachable
from ..caminos import caminos_simples_st_prioritize_minlenFIFO
from ..caminos import DFS


def invertir_camino(D, P):
    """Dado un digrafo D y un s-t camino P, invertir_camino(D,P)
       retorna el digrafo D <---P
       :param D:
       :type D: objeto de la clase grafo
       :param P: camino
       :lista con los nodos que conforman el camino
       """

    assert D.directed
    for i in range(len(P) - 1):
        e = (P[i], P[i + 1])
        D.remove_edge(e)
        e_inv = inv(e)
        D.add_edge(e_inv)
    return D


def augmenting_paths(D, s, t):
    """Dado un digrafo D y vértices s,t, augmenting_paths ejecuta el
        algoritmo descrito en 9.2 (Ford-Fulkerson for paths)
           :param D:
           :type D: objeto de la clase grafo
           :param s:
           :type nodo
           :param t:
           :type nodo
           """
    contador = 0
    B = set()

    while True:
        try:
            path = minimum_directed_path(D, s, t)

            arcos_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

            for e in arcos_path:
                if e in B:
                    B.remove(e)
                else:
                    B.add(e)
            D = invertir_camino(D, path)

            contador += 1

        except ValueError:
            return D, B


def describe_path_packing(G, s, t):
    contador = 0
    packing = []


    while G.aristas:

        path = get_naive_semieulerian_path(G, s, t)
        packing.append(path)
        contador += 1
        arcos_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]




    return packing





def describe_cut(G, D, s):

    E, U = caminos_simples_prioritize_minlength_fifo_reachable(D, s)
    H = G.delta_out(U)
    return H


def menger_path_cut(G, s, t):


    G1 = G.__copy__()
    D, B = augmenting_paths(G1, s, t)

    new_G = Grafo(D.vertices, list(B), directed=True)
    print('en menger_path_cut_arcos D', D.aristas)
    print('en menger path cut D vertices',D.vertices)
    print('en menger path cut Gnewaristas', new_G.aristas)

    packing = describe_path_packing(new_G, s, t)
    cut = describe_cut(G, D, s)

    return packing, cut




def blocking_collection(G, s, t):
    """

    :param G: An acyclic digraph G=(V,A)
    :param s: Source vertex
    :param t: Target node
    :return:  A blocking collection of arc-disjoint s-t paths founded in time O(m) Theorem 9.4 Schrijver
    """

    G1 = G.__copy__()
    blocking = list()
    dfs = DFS()

    while True:
        aristas, padres, path = dfs.do_dfs(tree=G1, root=s, destino=t) # aristas hace las veces de A' y path es el st camino
        #print('este es path', path)
        #print('este es A', aristas)
        if len(path) <= 1:
            break
        else:
            blocking.append(path)
            for e in aristas:
                G1.remove_edge(e)

    return blocking


def reverse_blocking_collection(D,s,t):

    # Encontrar  \alpha(D)
    st_caminos, st_shortest, alpha_grafo = caminos_simples_st_prioritize_minlenFIFO(D, s, t)
    print('este es alpha_grafo', alpha_grafo)
    # Formar el grafo  \hat(D)=(V,\alpha(D))
    D_gorro = Grafo(D.vertices, list(alpha_grafo), directed=True)
    # Encontrar una blocking collection en \hat(D) {\P_, \cdots, P_k \}
    blocking = blocking_collection(D_gorro, s, t)
    # Construir D''=D <--P_1<----....<---P_k

    for P in blocking:
        print('Este es un camino del blocking', P)

        D_prima2 = invertir_camino(D, P)
        D=D_prima2

    return D_prima2, blocking


def multiple_augmented_paths(D,s,t):

    """
    Dinits speed up for path packing
    :param D: A digraph
    :param s: source vertex
    :param t: target vertex
    :return: D_{final}
    """

    B = set()
    while True:
        try:
            D, blocking = reverse_blocking_collection(D,s,t)
            for path in blocking:
                arcos_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

                for e in arcos_path:
                    if e in B:
                        B.remove(e)
                    else:
                        B.add(e)

        except:
            return D,B


def menger_path_cut_speedup(G,s,t):
    G1 = G.__copy__()
    D_final, B = multiple_augmented_paths(G1, s, t)

    new_G = Grafo(D_final.vertices, list(B), directed=True)
    #print('en menger_path_cut_speedup_arcos D', D_final.aristas)
    #print('en menger path cut D_speedup vertices', D_final.vertices)
    #print('en menger path cut_speedup Gnewaristas', new_G.aristas)

    packing = describe_path_packing(new_G, s, t)
    cut = describe_cut(G, D_final, s)

    return packing, cut

















