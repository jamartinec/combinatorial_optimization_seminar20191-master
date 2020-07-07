# coding: utf8
# Copyright: MathDecision

from copy import deepcopy

class Grafo():
    """ En esta implementacion inicializamos un grafo a partir de sus vertices y
        aristas. Consultar los vecinos de un vertice opera en tiempo O(1).

        Podemos agregar informacion adicional a las aristas.

        Los nombres de los vertices del grafo deben ser enteros o strings.

    """

    def __init__(self, vertices, aristas, directed=False):

        self.vertices = vertices
        """ Vertices del grafo """

        self.num_vertices = len(self.vertices)
        """ Numero de vertices del grafo """

        self.directed = directed
        """ Indica si el grafo es dirigido o no"""

        self.aristas = set(aristas)
        """ Aristas del grafo """

        self._vecinos = dict()
        """ Vecinos de cada vertice del grafo (solo para grafos no dirigidos) """

        self._succesors = dict()
        """ Sucesores de cada vertice (solo para grafos dirigidos)"""

        self._predecessors = dict()
        """ Predecesores de cada vertice (solo para grafos dirigidos) """

        self._info_aristas = dict()
        """ Informacion adicional de las aristas del grafo """

        # Inicializacion de la estructura de datos _vecinos
        if self.directed:
            self._succesors = {v: set() for v in vertices}
            self._predecessors = {v: set() for v in vertices}
            for v, w in aristas:
                self._succesors[v].add(w)
                self._predecessors[w].add(v)
        else:
            self._vecinos = {v: set() for v in vertices}
            for v, w in aristas:
                self._vecinos[v].add(w)
                self._vecinos[w].add(v)

        # Inicializacion de la estructura de datos _info_aristas
        self._info_aristas = {(v, w): dict() for v, w in aristas}
        if not self.directed:
            self._info_aristas.update({(w, v): dict() for v, w in aristas})

    def vecinos(self, v):
        return self._vecinos[v]

    def succesors(self, v):
        return self._succesors[v]

    def predecessors(self, v):
        return self._predecessors[v]

    def remove_edge(self, e):
        if self.directed:
            self.aristas.remove(e)
            del self._info_aristas[e]
            v, w = e
            self._succesors[v].remove(w)
            self._predecessors[w].remove(v)
        else:
            raise NotImplementedError



    ## Esta función (add_edge) la agregué

    def add_edge(self, e):
        if self.directed:
            self.aristas.add(e)
            self._info_aristas.update({e: dict()})
            u, v = e
            self._succesors[u].add(v)
            self._predecessors[v].add(u)
        else:
            raise NotImplementedError




    def add_info(self, e, key, val):
        """  """
        v, w = e
        if (v, w) not in self._info_aristas:
            raise ValueError('Arista {} no existente'.format(e))
        self._info_aristas[(v, w)][key] = val
        if not self.directed:
            self._info_aristas[(w, v)][key] = val

    def get_info(self, e, key):
        v, w = e
        if (v, w) not in self._info_aristas:
            raise ValueError('Arista {} no existente'.format(e))
        return self._info_aristas[(v, w)][key]


    def delta_out(self,U):

        if self.directed:
            delta = set()
            for u in U:
                for w in self._succesors[u]:
                    if w not in U:
                        delta.add((u, w))
            return delta
        else:
            raise NotImplementedError


    def __str__(self):
        return str(self._vecinos)

    def __copy__(self):
        return deepcopy(self)


class Node():

    def __init__(self, name):

        self.name = name
        self._sucessors = set()


    def add_sucessor(self, node):
        self._sucessors.add(node)

    def get_succesors(self):
        return self._sucessors


class LinkedNode():

    def __init__(self, name):
        self.name = name
        self.successor = None

    def linkto(self, node):
        self.successor = node

    def tolist(self):
        lista = [self.name]
        current_node = self
        while current_node.successor is not None:
            current_node = current_node.successor
            if current_node == self:
                break
            lista.append(current_node.name)
        return lista



