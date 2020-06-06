import math
from camino import Camino
from grafo import DAG

def caminos_minimos(grafo, v):
  """ Retorna los caminos minimos del grafo que comienzan en v.
      La complejidad en tiempo de este algoritmo es O(N) y en espacio es O(Nd) donde
      N es el numero de caminos minimos del grafo que comienzan en v y d es la longitud
      promedio de tales caminos minimos.

      V es un conjunto que contiene los vértices previamente visitados.
      H es una lista que en cada iteración contiene los caminos que se intentarán extender.
      caminos es una lista en la que se irán guardando todas las extensiones simples. Al final contendrá todos los
      caminos mínimos del grafo G.


  """
  nuevo_camino = Camino([v])
  caminos = [nuevo_camino]
  H = [nuevo_camino]
  V = set([v])
  while H: # mientras hayan caminos para ser extendidos
    actH = []
    actV = set()
    for camino in H:
      cola = camino.tail()
      for w in grafo.vecinos(cola): #iterando sobre un conjunto
        if w not in V:
          actV.add(w)
          nuevo_camino = camino.extend(w, copy=True)
          actH.append(nuevo_camino) # a
          caminos.append(nuevo_camino)
    # al salir del for, actH contiene todas las extensiones unitarias que fue posible realizar a partir
    # de caminos contenidos en H. Estos a su vez son conforman los caminos que tratará de extenderse en la próxima iteración
    H = actH
    V.update(actV)
  return caminos


def caminos_dag(grafo, v):
  """ Retorna el DAG inducido por los caminos minimos del grafo que comienzan en v.

      V es un conjunto que contiene todos los vértices ya incluidos en el DAG.
      T es un conjunto que en cada iteración contiene los vértices cuyos vecinos serán explorados
  """
  dag = DAG(grafo.vertices, [])
  V = set([v])
  T = set([v])
  dist = 0
  dag.add_info(v, 'distancia', dist)
  while T:
    dist += 1
    actT = set()
    for u in T:
      for w in grafo.vecinos(u):
        if w not in V:
          dag.agregar_arista(u, w)
          dag.add_info(w, 'distancia', dist)
          actT.add(w)
    T = actT
    V.update(actT)
  return dag


def get_niveles_version_uno(grafo, s):
  niveles = []
  niveles.append([s])
  while niveles[-1]:
    new_nivel = []
    for u in niveles[-1]:
      for v in grafo.vecinos(u):
        contenencia = False
        for nivel in niveles:
          if v in nivel:
            contenencia= True
        if not contenencia:
          new_nivel.append(v)
    niveles.append(new_nivel)
  return niveles


def get_niveles_version_dos(grafo,s):

    niveles=[]
    visited=set()
    niveles.append({s})
    visited.add(s)
    while niveles[-1]:
        new_nivel = set()
        for u in niveles[-1]:
            for v in grafo.vecinos(u):
                if v not in visited:
                    new_nivel.add(v)
                    visited.add(v)
        niveles.append(new_nivel)
    return niveles

def get_dist_niveles(grafo,s,v):
    if (s not in grafo.vertices ) or (v not in grafo.vertices):
        raise ValueError
    else:
        niveles = get_niveles_version_dos(grafo,s)
        dist= math.inf
        for i in range(len(niveles)):
            if v in niveles[i]:
                dist = i
    return dist

def get_camino_niveles(grafo,s,v):
    if (s not in grafo.vertices ) or (v not in grafo.vertices):
        raise ValueError
    else:
        niveles = get_niveles_version_dos(grafo,s)
        path=[]
        d = math.inf
        for i in range(len(niveles)):
            if v in niveles[i]:
                d = i
        if d == math.inf:
            print('no existe un camino')
        else:
            p = d
            vertice = v
            path.append(vertice)

            while p>0:
                p = p-1
                for w in niveles[p]:
                    if vertice in grafo.vecinos(w):
                        vertice = w
                        path.append(vertice)
                        break
                    else:
                        pass
            path.reverse()

    return path












def caminos_peso_minimo(grafo, v):

  """ Retorna los caminos de peso minimo del grafo que comienzan en v.
      La complejidad en tiempo de este algoritmo es O(N) y en espacio es O(Nd) donde
      N es el numero de caminos de peso minimos del grafo que comienzan en v y d es la longitud
      promedio de tales caminos de peso minimo.

      H_k = Caminos de peso minimo de longitud <= k.
      H_{k + 1} = E(H_k) / I_{k + 1}
      I_k = Caminos p de longitud <= k tal que w(p) > F_k(tail(p))
      F_k(w) = Costo minimo de un camino de longitud <= k entre v y w
      F_{k + 1}(w) = min w(p): p esta en H_{k + 1} y tail(p) = w
  """

  H = [Camino([v])]
  caminos = [H]
  F = {w: float('inf') for w in grafo.vertices}
  F[v] = 0
  while H:
    EH = []
    for camino in H:
      w = camino.tail()
      for z in grafo.vecinos(w):
        if z not in camino:
          nuevo_camino = camino.extend(z, copy)
          EH.append(nuevo_camino)
    H = []
    for w in grafo.vertices:
      try:
        min_peso = min([camino.peso() for camino in EH if camino.tail() == w])
        H.extend([camino for camino in EH if camino.tail() == w and camino.peso() == min_peso])
      except ValueError:
        pass
    caminos.append(H)
  return caminos