from collections import deque
import itertools as its
from .camino import Camino





# Varias implementaciones que retornan todos los caminos simples a partir de un vertice dado

def caminos_simples(grafo, v, algoritmo=''):
    """ Retorna los caminos simples del grafo que comienzan en el vertice v.

    - prioritize_minlength_fifo: Este algoritmo extiende cada camino previamente construido de todas las formas
      posibles, teniendo cuidado de primero extender los caminos construidos de longitud minima. Esto lo
      realizamos mediante una cola FIFO. La complejidad en tiempo es O(N) y en espacio es O(N * d), donde N
      es el numero total de caminos simples del grafo y d es la longitud promedio de los caminos simples
      del grafo. Las caminos son hallados en orden de longitud.

    - prioritize_minlength: Este algoritmo extiende cada camino previamente construido de todas las formas
      posibles, teniendo cuidado de primero extender los caminos construidos de longitud minima. Esto lo realizamos 'buscando' los caminos de longitud minima en cada iteracion. La complejidad en tiempo es
      hasta O(N**2) y en espacio es O(N * d), donde N es el numero total de caminos simples del grafo y d es la longitud promedio de los caminos simples del grafo. Las caminos son hallados en orden de longitud.

    - prioritize_last: Este algoritmo extiende cada camino previamente construido de todas las formas
      posibles, en cada iteración prioriza para extensión el último camino extendido. La complejidad en tiempo es
      hasta O(N) y en espacio es O(Nd), donde N es el numero total de caminos simples del grafo y d es la longitud promedio de los caminos simples del grafo. Las caminos NO son hallados en orden de longitud.


    """
    if algoritmo == 'prioritize_minlength_fifo':
        caminos = caminos_simples_prioritize_minlength_fifo(grafo, v)
    elif algoritmo == 'prioritize_last':
        caminos = caminos_simples_prioritize_last(grafo, v)
    elif algoritmo == 'prioritize_minlength':
        caminos = caminos_simples_prioritize_minlength(grafo, v)
    else:
        raise NotImplementedError()
    return caminos


def caminos_simples_prioritize_last(grafo, v):
    """ Via extending the last discovered path """
    caminos = []
    stack = [Camino([v])]
    while stack:
        p = stack.pop()
        caminos.append(p)
        u = p.tail()
        for w in grafo.vecinos(u):
            if w not in p:
                stack.append(p.extend(w, copy=True))
    return caminos


def caminos_simples_prioritize_minlength(grafo, v):
    """ Via extending a path of minimum length """
    caminos = []
    stack = [Camino([v])]
    while stack:
        # The index in 'stack' of a path of minimum length (It will turn out to always be 0!)
        i, _ = min(enumerate(stack), key=lambda x: len(x[1]))
        p = stack.pop(i)
        caminos.append(p)
        u = p.tail()
        for w in grafo.vecinos(u):
            if w not in p:
                stack.append(p.extend(w, copy=True))
    return caminos


def caminos_simples_prioritize_minlength_fifo(grafo, v):
    """ Via extending a path of minimum length, using fifo queues for speed """

    caminos = []
    stack = deque([Camino([v])])
    while stack:
        p = stack.popleft()
        caminos.append(p)
        u = p.tail()
        for w in grafo.vecinos(u):
            if w not in p:
                stack.append(p.extend(w, copy=True))

    return caminos

def caminos_simples_prioritize_minlength_fifo_reachable(grafo, v):
    """ Via extending a path of minimum length, using fifo queues for speed """
    reachable = {v}
    caminos = []
    stack = deque([Camino([v])])
    while stack:
        p = stack.popleft()
        caminos.append(p)
        u = p.tail()
        print()
        for w in grafo.succesors(u):
            print('vecinos de u', w)
            if w not in p:
                stack.append(p.extend(w, copy=True))
                reachable.add(w)

    return caminos, reachable




class DFS(object):
    def do_dfs(self, tree, root,destino):
        """
        """
        self.start_finish_time = {}
        self.visited = set()
        self.aristasinc = set() # para llevar un registro de las aristas visitadas
        self.time = its.count(0)
        self.path = list() # camino root-destino

        self.parent = dict()
        for v in tree.vertices:
            self.parent[v] = None


        if root not in self.visited:
            self.dfs_traverse_iterative(tree, root,destino)
        #for (r, (s, f)) in self.start_finish_time.items():
            # print('Root: {}\n\t{}\n\t{}'.format(r,sorted(s.items()),sorted(f.items())))
        apuntador = self.parent[destino]
        self.path.append(destino)
        while apuntador != None:
            self.path.append(apuntador)
            apuntador = self.parent[apuntador]
        self.path.reverse()


        return self.aristasinc, self.parent,self.path


    def dfs_traverse_iterative(self, tree, root, destino, order=None):
        """
        """
        stack = [root]
        s = {}
        f = {}  # the times you finish visiting things.
        while stack:

            t = next(self.time)
            u = stack[-1]  # Don't pop things off yet you need to go deep in first
            if u != destino:
                if u not in self.visited:
                    s[u] = t  # preorder nodes here
                self.visited.add(u)  # Visit when you see things at the top of the stack
                finished = True  # Tells you when a node's neighbours are all visited.
                for v in tree.succesors(u):
                    if v not in self.visited:
                        finished = False
                        stack.append(v)
                        #self.aristasinc.add((u,v))
                        self.parent[v]= u
                if self.parent[u] != None:
                    self.aristasinc.add((self.parent[u], u))


                # Done with all the neighbours of the node.
                if finished and stack:
                    u = stack.pop()  # post order nodes here
                    if u not in f:
                        f[u] = t

            else:
                s[u] = t  # preorder nodes here
                self.visited.add(u)  # Visit when you see things at the top of the stack
                finished = True  # Tells you when a node's neighbours are all visited.
                f[u] = t
                self.aristasinc.add((self.parent[u], u))
                break


        self.start_finish_time[root] = (s, f)


def caminos_simples_st_prioritize_minlenFIFO(grafo, s,t):
    """
    Via extending a path of minimum length, using fifo queues for speed
    Un camino no se extiende si este ya termina en t.
    Guardamos en caminos todos los caminos que terminen en t y los ordenamos según longitud creciente
    """

    st_caminos = []
    st_shortest = []
    stack = deque([Camino([s])])
    while stack:
        p = stack.popleft()
        u = p.tail()
        if u == t:
            st_caminos.append(p)
        # Una vez se ha alcanzado t, no seguimos extendiendo
        if u!= t:
            for w in grafo.succesors(u):
                if w not in p:
                    stack.append(p.extend(w, copy=True))
    if len(st_caminos)>=1:
        shortest = min(len(camino) for camino in st_caminos)
        for camino in st_caminos:
            if len(camino)== shortest:
                st_shortest.append(camino)

        alpha_grafo = set()
        for camino in st_shortest:
            for e in camino.lista_arcos():
                alpha_grafo.add(e)
    else:
        raise ValueError

    return st_caminos, st_shortest, alpha_grafo