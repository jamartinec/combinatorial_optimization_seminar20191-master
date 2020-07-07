from collections import deque
from grafo import Grafo 
from camino import Camino 
import math


def DFS(G, v):
    mark = dict()
    parent = dict()
    for vertice in G.vertices:
        mark[vertice] = 0
    mark[v] = 1

    for w in G.vecinos(v):
        if mark[w] == 0:
            parent[w] = v
            DFS(G, w)
    return parent


# pre-order and Postorder

def DFS_clock(G,v,clock): ##### Este está malo, arreglarlo.

    G.marca[v] = 1
    clock = clock + 1
    G.pre[v] = clock
    for w in G.vecinos(v):
        if G.marca[w] == 0:
            G.parent[w] = v
            clock = DFS_clock(w, clock)
    clock = clock + 1
    G.post[v] = clock
    return clock


def INITSSSP(grafo, s):
    # creamos un diccionario para almacenar la distancia a s
    dist = dict()
    pred = dict()
    dist[s] = 0
    pred[s] = None
    for vertice in grafo.vertices:
        if not vertice == s:
            dist[vertice] = math.inf
            pred[vertice] = None
    return {1: dist, 2: pred}


def BF(G, s):
    l = INITSSSP(G, s)
    dist = l[1]
    pred = l[2]
    # implementar una cola de prioridad (FIFO)
    q = deque()
    q.append(s)
    while q:
        u = q.pop()
        for v in G.vecinos(u):
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                pred[v] = u
                q.append(v)
    return dist


import itertools as its


class DFS(object):
    def do_dfs(self, tree, root):
        """
        """
        self.start_finish_time = {}
        self.visited = set()
        self.time = its.count(0)
        if root not in self.visited:
            self.dfs_traverse_iterative(tree, root)
        for (r, (s, f)) in self.start_finish_time.iteritems():
            print
            'Root: {}\n\t{}\n\t{}'.format(
                r,
                sorted(s.iteritems()),
                sorted(f.iteritems()))

    def dfs_traverse_iterative(self, tree, root, order=None):
        """
        I worked this out on paper with an example from CLRS.  You need to record the start and end
        times carefully because you are using an array as a stack instead of function calls.
        """
        stack = [root]
        s = {}
        f = {}  # the times you finish visiting things.
        while stack:
            t = self.time.next()
            u = stack[-1]  # Don't pop things off yet you need to go deep in first
            if u not in self.visited:
                s[u] = t  # preorder nodes here
            self.visited.add(u)  # Visit when you see things at the top of the stack
            finished = True  # Tells you when a node's neighbours are all visited.
            for v in tree[u]:
                if v not in self.visited:
                    finished = False
                    stack.append(v)

            # Done with all the neighbours of the node.
            if finished and stack:
                u = stack.pop()  # post order nodes here
                if u not in f:
                    f[u] = t
        self.start_finish_time[root] = (s, f)


def test_dfs_iterative():
    tree = {
        'u': ['x', 'v'],
        'v': ['y'],
        'y': ['x'],
        'x': ['v'],
        'w': ['y', 'z'],
        'z': ['z']
    }
    dfs = DFS()
    dfs.do_dfs(tree=tree, root='u')


if '__main__' in __name__:
    test_dfs_iterative()