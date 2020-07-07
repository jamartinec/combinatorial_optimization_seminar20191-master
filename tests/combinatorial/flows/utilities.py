# coding: utf8
# Copyright: MathDecision


"""

Un flujo f es una función de las aristas de un grafo a los reales positivos y que
satisface la ecuación de balance en cada vértice 'interior' del grafo.
Los vértices 'interiores' son los que son diferentes a un conjunto preseleccionado
('la frontera'), el cual puede ser vacio. En tal caso, decimos que f es un flujo
con frontera S.

Una representación posible de un flujo es un diccionario que tiene como claves
las aristas del grafo.

"""

from ..graph import Grafo
from ..minpath import minimum_directed_path
from ..utils import inv
from ..caminos import DFS
from ..caminos import caminos_simples_st_prioritize_minlenFIFO


def is_flow(f, G, S, cap=None):
    """ Verifica que la función f que va de las aristas de G en R sea efectivamente
    un flujo con frontera S.

    Si cap no es None, verifica además que el flujo cumpla las condiciones
    de capacidad especificadas por la función cap

    :param f:
    :type f: dict
    :param G:
    :type G: Grafo
    :param S:
    :type S: set
    """

    assert G.directed

    # Condición de positividad
    for e in G.aristas:
        if f[e] < 0:
            return False

    # Condición de capacidad
    if cap is not None:
        for e in G.aristas:
            if f[e] > cap[e]:
                return False

    # Condición de conservación
    for v in G.vertices:
        if v not in S:
            inflow = sum(f[(w, v)] for w in G.predecessors(v))
            outflow = sum(f[(v, w)] for w in G.succesors(v))
            if inflow != outflow:
                return False

    return True


def residual_graph(f, c, G):
    """ Crea un nuevo grafo Df con los mismos vértices de G, y tal que, dada
    una arista e en G:
    - e pertenece a Df si f(a) < c(a)
    - e^(-1) pertenece a Df si f(a) > 0
    """
    vertices = G.vertices
    aristas = []
    for e in G.aristas:
        if f[e] < c[e]:
            aristas.append(e)
        if f[e] > 0:
            aristas.append(inv(e))
    return Grafo(vertices, aristas, directed=True)


def _path_directions(G, P):
    """ Esta función toma un path no dirigido en G y nos retorna una función que,
    para cada arista de P nos da su dirección en P.
    Ejemplo, Supongamos las aristas de G son (1, 2), (3, 2), (4, 3), (4, 5), (2, 4).
    P = [1, 2, 3, 4, 5] es un camino no dirigido cuyas aristas son.
    (1, 2), (3, 2), (4, 3) y (4, 5). Las direcciones de estas aristas en P, son:
    1, -1, -1 y 1, respectivamente.
    Se asume que G no tiene ciclos de longitud 1 o 2.
    """
    phi = dict()
    for u, v in zip(P[:-1], P[1:]):
        if (u, v) in G.aristas:
            phi[(u, v)] = 1
        elif (v, u) in G.aristas:
            phi[(v, u)] = -1
    return phi


def improve_flow(f, c, G, P):
    """ Esta función toma un path no dirigido en G, de s a t y nos retorna la mejor
    modificación de f sobre el camino P.
    f: diccionario de flujo
    c: diccionario de capacidades
    G: un digrafo
    P: camino no dirigido ingresado como una lista

    """
    phi = _path_directions(G, P)
    epsilon = float('inf')
    for e, signo in phi.items():
        if signo == 1:
            epsilon = min(epsilon, c[e] - f[e])
        else:
            epsilon = min(epsilon, f[e])
    for e, signo in phi.items():
        f[e] = f[e] + signo * epsilon
    return f, epsilon



# def residual_action(f, c, G):
#     """ Modifica el grafo G, para obtener un nuevo grafo Df con los mismos
#     vértices de G, y tal que, dada una arista e en G:
#     - e pertenece a Df si f(a) < c(a)
#     - e^(-1) pertenece a Df si f(a) > 0
#     """
#     vertices = G.vertices
#     for e in G.aristas:
#         if f[e] < c[e]:
#             aristas.append(e)
#         if f[e] > 0:
#             aristas.append(inv(e))
#     return Grafo(vertices, aristas, directed=True)


def maximum_flow(grafo, cap, s, t):
    """

    :param grafo:
    :type grafo: Grafo
    :param cap:
    :return:
    """

    # Partimos de un flujo trivial

    # Calculamos el residual respecto a ese flujo

    # Hallamos un camino de s a t en el residual

    # Si no hay tal camino, terminamos

    # De otra forma, mejoramos el flujo y repetimos

    f = {e: 0 for e in grafo.aristas}
    while True:
        residual = residual_graph(f, cap, grafo)
        try:
            path = minimum_directed_path(residual, s, t)
        except ValueError:
            return f
        f, eps = improve_flow(f, cap, grafo, path)


def blocking_flow(G,s,t,c):
    """
    :param G: Un digrafo
    :param s: source vertex (source)
    :param t: target vertex (sink)
    :param c: capacity function as a dictionary
    :return: Devuelve un blocking flow
    """

    G1 = G.__copy__()
    blocking = list()
    dfs = DFS()

    blocking_f = dict()#inicializamos el flujo
    for e in G1.aristas:
        blocking_f[e] = 0
    menchoset = set()

    while True:
        #print('ESTAS SON LAS ARISTAS DE G1 AL ENTRAR AL WHILE', G1.aristas)
        aristas, padres, path = dfs.do_dfs(tree=G1, root=s, destino=t)
        # aristas hace las veces de A' y path es el st camino
        #print('este es A', aristas)
        #print('este es path', path)
        # Encontrar el máximo flujo max_f que puede enviarse a través de P

        if len(path) <= 1:
            break
        else:
            arcos_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            max_f = min([c[e] for e in arcos_path])
            print('este es el flujo máximo a enviar por P', max_f)
            input("Press Enter to continue...")
            for e in arcos_path:
                c[e] = c[e]-max_f
            new_aristas = aristas - set(arcos_path)
            #print('este es new_aristas', new_aristas)


            for e in list(G1.aristas):
                #print('arista evaluada',e)
                if ((e in new_aristas) or (c[e]==0)) :
                    G1.aristas.remove(e)
                    menchoset.add(e)
                    #print('este es G1 aristas',G1.aristas)
            for e in arcos_path:
                blocking_f[e] = blocking_f[e] + max_f

        #print('ESTAS SON LAS ARISTAS DE G1', G1.aristas)
        G1 = Grafo(G1.vertices, list(G1.aristas), directed=True)

    return blocking_f, G1, menchoset,c



def augmenting_along_flows(grafo, f, cap, s, t):


    #f_prima = dict()
    #for e in grafo.aristas:
        #f_prima[e] = 0

    while True:
        try:
            # obtener el grafo residual D_f=(V,A_f)
            D_f = residual_graph(f, cap, grafo)
            print('estas son las aristas de D_f el residual', D_f.aristas)
            # definimos una nueva función de capacidad cap_f sobre A_f
            cap_f = dict()
            for a in grafo.aristas:
                if a in set(D_f.aristas):
                    cap_f[a] = cap[a] - f[a]
                if inv(a) in set(D_f.aristas):
                    cap_f[inv(a)] = f[a]
            #print('este es cap_f', cap_f)

            # Encontrar  \alpha(D)
            st_caminos, st_shortest, alpha_grafo = caminos_simples_st_prioritize_minlenFIFO(D_f, s, t)
            #print('este es alpha grafo',alpha_grafo)
            # Formar el grafo  \hat(D)=(V,\alpha(D))
            nuevo_grafo = Grafo(grafo.vertices, list(alpha_grafo), directed = True)
            # Encontrar un blocking flow en (V,\alpha(D_f)) sujeto a cap_f
            g,G1,menchoset,c = blocking_flow(nuevo_grafo, s, t, cap_f)
            print('este es el blocking g',g)
            #print('aristas de G1',G1.aristas)
            #print('menchoset',menchoset)


            # ESTO ES LO QUE ESTÁ MALO ¿cambiar D_f por G_1 (aristas abjajo)
            for e in grafo.aristas:

                if ((e  in nuevo_grafo.aristas) and (inv(e) in nuevo_grafo.aristas)):
                    f[e] = f[e] + g[e] - g[inv(e)]
                elif ((e  in nuevo_grafo.aristas) and (inv(e) not in nuevo_grafo.aristas)):
                    f[e] = f[e] + g[e]
                elif ((e not in nuevo_grafo.aristas) and (inv(e)  in nuevo_grafo.aristas)):
                    f[e] = f[e] - g[inv(e)]

            good_aristas = grafo.aristas-menchoset
            print('el f', f)

            grafo = Grafo(G1.vertices,list(good_aristas),directed=True)


        except:
            print('FLUJO',f)
            return f













