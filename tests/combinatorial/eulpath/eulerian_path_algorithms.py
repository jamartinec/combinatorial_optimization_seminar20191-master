# coding: utf8
# Copyright: MathDecision

from ..graph import Grafo
from ..graph import LinkedNode
from ..graph import Node
from ..utils import query_from_set


def verify_flow_condition(graph, s, t):
    """ Verifica la condición de flujo

    :param graph:
    :type graph: Grafo
    """
    assert graph.directed
    for v in graph.vertices:
        if v == s:
            if not (len(graph.succesors(v)) - len(graph.predecessors(v)) == 1):
                return False
        elif v == t:
            if not (len(graph.succesors(v)) - len(graph.predecessors(v)) == -1):
                return False
        else:
            if not (len(graph.succesors(v)) == len(graph.predecessors(v))):
                return False
    return True


def get_naive_semieulerian_path(graph, s, t):
    """ Halla un camino de s a t mediante una caminata arbitraria
        (el grafo debe satisfacer la condición de flujo)  """
    #assert verify_flow_condition(graph, s, t) == True

    v = s
    camino =[v]

    while graph.succesors(v):
        w = query_from_set(graph.succesors(v))
        graph.remove_edge((v, w))
        v = w
        camino.append(w)
    return camino


def get_naive_semieulerian_path_and_stack(graph, s, t, stack):
    """ Halla un camino de s a t mediante una caminata arbitraria
        (el grafo debe satisfacer la condición de flujo)
        Nos devuelve además, una lista con vértices de los que posiblemente
        se pueden generar mas caminos.
    """
    v = s
    camino = [v]
    print('camino', camino)
    while graph.succesors(v):

        w = query_from_set(graph.succesors(v))
        # En el stack se agregan los vértices visitados durante la caminata, que después de
        # salir de ellos, aun tengan aristas salientes sin utilizar.
        if len(graph.succesors(v)) > 1:
            stack.append(v)
        graph.remove_edge((v, w))
        v = w
        camino.append(w)

    return camino


def get_naive_semieulerian_path_enriched(graph, s, t):
    """ El grafo debe satisfacer la condición de flujo  """
    successor_count = dict()

    # Vertice inicial
    v = s

    # Inicializar nodo
    v_node = Node(v)
    esqueleto = v_node

    # Inicializar exit_vertices
    exit_vertices = {v}

    while graph.succesors(v):

        # todo: limpiar, se puede cambiar por query_from_set
        #for _ in graph.succesors(v):
        #    w = _
        #    break
        w = query_from_set(graph.succesors(v))
        graph.remove_edge((v, w))
        successor_count[v] = len(graph.succesors(v))
        if successor_count[v] == 0:
            # el vértice v no es un candidato para retomar la caminata
            exit_vertices.remove(v)

        # Añadir nuevo nodo
        w_node = Node(w)
        v_node.add_sucessor(w_node)

        # Actualizar nuevo vertice del recorrido
        v = w
        exit_vertices.add(v)

    successor_count[v] = len(graph.succesors(v))
    exit_vertices.remove(v)

    return esqueleto, successor_count, exit_vertices

def eulerian_path(graph, s, t):
    """ El grafo debe satisfacer la condición de flujo

    :type graph: Grafo

    Implementación algoritmo de Hierholzer

    """
    assert verify_flow_condition(graph, s, t) == True
    node_dict = {s: LinkedNode(s), t: LinkedNode(t)}
    initial_node = node_dict[s]
    stack = []
    path = get_naive_semieulerian_path_and_stack(graph, s, t, stack)
    # verifique que el camino semi euleriano termina en t
    assert path[-1] == t
    current_node = node_dict[s]
    end_node = node_dict[t]
    for v in path[1:-1]:
        new_node = LinkedNode(v)
        current_node.linkto(new_node)
        current_node = new_node
        node_dict[v] = new_node
    current_node.linkto(end_node)
    # lo anterior reconstruye el camino semi euleriano obtenido más arriba, pero ahora cada nodo
    # es un objeto de la clase LinkedNode
    while stack:
        s = stack.pop()
        print('este es s en eulerian_path',s)
        if len(graph.succesors(s)) > 0:
            path = get_naive_semieulerian_path_and_stack(graph, s, s, stack)
            assert path[-1] == s
            current_node = node_dict[s]
            end_node = node_dict[s].successor
            for v in path[1:]:
                new_node = LinkedNode(v)
                current_node.linkto(new_node)
                current_node = new_node
                node_dict[v] = new_node
            current_node.linkto(end_node)
    return initial_node.tolist()










if __name__ == '__main__':

    graph = Grafo([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)], directed=True)

    verify_flow_condition(graph, 1, 4)

    path = eulerian_path(graph, 1, 4)

    print(path)

    graph = Grafo(['s', 1, 2, 3, 't', 4, 5],
                  [('s', 1), (1, 2), (2, 3), (3, 't'), (1, 4), (4, 3), (3, 5),
                   (5, 1)], directed=True)

    verify_flow_condition(graph, 's', 't')

    path = eulerian_path(graph, 's', 't')

    print(path)
