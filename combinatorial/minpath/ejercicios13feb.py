

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
# prueba gitlab SSSSS