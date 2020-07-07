# coding: utf8



"""

Una función de longitud l: A ---> R  es una función de las aristas de un grafo a los reales

Una representación posible de una función de longitud es un diccionario que tiene como claves
las aristas del grafo y como valor correspondiente la longitud de la arista

"""

import math
import heapq
import bisect

#from pqdict import pqdict

from ..graph import Grafo
from ..minpath import minimum_directed_path
from ..utils import inv
from ..caminos import DFS
from ..caminos import caminos_simples_st_prioritize_minlenFIFO



def is_nonnegative_length(G, l):
    """ Verifica que la función l que va de las aristas de G en R sea no negativa

        :param l:
        :type l: dict
        :param G:
        :type G: Grafo
        """

    assert G.directed

    # Condición de no negatividad
    for e in G.aristas:
        if l[e] < 0:
            return False

    return True

def Dijkstra(G,l,s):
    """ Ejecuta el algoritmo de Dijkstra sobre un digrafo G con función de
        longitud l, que toma valores enteros no negativos.
        Este algoritmo retorna para cada vértice v en G, la longitud del s-v
        camino más corto y también retorna un árbol de caminos más cortos.
        El estructura de datos fundamental en Dijsktra es la priority queue.
        En esta implementación se usa el módulo pqdict.

            :param l:
            :type l: dict
            :param G:
            :type G: Grafo
            :param s:
            :type s: int or string
            """
    # Esta implementación es muy costosa en espacio:
    # Usamos un conjunto S para guardar los nodos cuya etiqueta es definitiva
    # es decir, aquellos que en determinada iteración tuvieron la menor etiqueta
    # Usamos un pqdict (implementación externa no nativa de python) como cola de
    # prioridad, el cual va disminuyendo su extensión conforme se hace pop del elemento
    # mínimo. En el diccionario label guardamos la distancia definitiva.
    S = set()
    pred = dict()
    n = G.num_vertices
    d = pqdict({vertice: float('inf') for vertice in G.vertices})
    label = {vertice: float('inf') for vertice in G.vertices}
    d[s] = 0
    label[s] = 0
    pred[s] = None
    while len(S)< n:


        (u2add, dist_min) = d.popitem()
        label[u2add] = dist_min
        #u2add = min(d.keys() - S, key=lambda _: d[_]) #Esto no está implementado como Priority queue
        # returns the key in d.keys()-S such that is value is the minimum one.
        # retorna el vertice u2add tal que su etiqueta es mínima en \bar{S} = V-S
        S.add(u2add)
        for uvec in G.succesors(u2add):
            print('uvec es',uvec)

            if uvec not in S: # si uvec no ha salido

                if  d[uvec] > dist_min + l[(u2add,uvec)]:
                    d[uvec] = dist_min + l[(u2add,uvec)]
                    pred[uvec] = u2add

    print(label)
    return label


def Reverse_Dijkstra(G,l,t):
    """ Ejecuta el algoritmo de Dijkstra Reverso sobre un digrafo G con función de
        longitud l, que toma valores enteros no negativos.
        Este algoritmo retorna para cada vértice v en G, la longitud del v-t
        camino más corto y también retorna un árbol de caminos más cortos.
        El estructura de datos fundamental en Dijsktra es la priority queue.
        En esta implementación se usa el módulo pqdict.

            :param l:
            :type l: dict
            :param G:
            :type G: Grafo
            :param t:
            :type t: int or string
            """
    # Esta implementación es muy costosa en espacio:
    # Usamos un conjunto S para guardar los nodos cuya etiqueta es definitiva
    # es decir, aquellos que en determinada iteración tuvieron la menor etiqueta
    # Usamos un pqdict (implementación externa no nativa de python) como cola de
    # prioridad, el cual va disminuyendo su extensión conforme se hace pop del elemento
    # mínimo. En el diccionario label guardamos la distancia definitiva.

    S = set()
    succ = dict()
    n = G.num_vertices
    d = pqdict({vertice: float('inf') for vertice in G.vertices})
    label = {vertice: float('inf') for vertice in G.vertices}
    d[t] = 0
    label[t] = 0
    succ[t] = None
    while len(S)< n:


        (u2add, dist_min) = d.popitem()
        label[u2add] = dist_min
        #u2add = min(d.keys() - S, key=lambda _: d[_]) #Esto no está implementado como Priority queue
        # returns the key in d.keys()-S such that is value is the minimum one.
        # retorna el vertice u2add tal que su etiqueta es mínima en \bar{S} = V-S
        S.add(u2add)
        for uvec in G.predecessors(u2add):
            print('uvec es',uvec)

            if uvec not in S: # si uvec no ha salido

                if  d[uvec] > dist_min + l[(uvec,u2add)]:
                    d[uvec] = dist_min + l[(uvec,u2add)]
                    succ[uvec] = u2add

    print(label)
    return label



def Bidirectional_Dijkstra(G,l,s,t):
    """ Ejecuta el algoritmo de Dijkstra Bidireccional sobre un digrafo G con función de
        longitud l, que toma valores enteros no negativos.
        Este algoritmo retorna para cada vértice v en G, la longitud del v-t
        camino más corto y también retorna un árbol de caminos más cortos.
        El estructura de datos fundamental en Dijsktra es la priority queue.
        En esta implementación se usa el módulo pqdict.

            :param l:
            :type l: dict
            :param G:
            :type G: Grafo
            :param s:
            :type s: int or string
            :param t:
            :type t: int or string
            """
    # Esta implementación es muy costosa en espacio:
    # Usamos un conjunto S para guardar los nodos cuya etiqueta es definitiva en el
    # Dijkstra hacia adelante. Usamos S_prima para guardar los nodos cuya etiqueta es
    # definitiva en el Dijkstra hacia atrás.
    # Usamos dos pqdict (implementación externa no nativa de python) como cola de
    # prioridad para la búsqueda hacia adelante y la búsqueda hacia atrás,
    # los cuales van disminuyendo su extensión conforme se hace pop del elemento
    # mínimo. En los  diccionarios label guardamos la distancia definitiva hacia
    # adelante y hacia atrás.



    S = set()
    S_prima = set()
    d = pqdict({vertice: float('inf') for vertice in G.vertices})
    d_prima = pqdict({vertice: float('inf') for vertice in G.vertices})
    label = {vertice: float('inf') for vertice in G.vertices}
    label_prima = {vertice: float('inf') for vertice in G.vertices}
    d[s] = 0
    label[s] = 0
    d_prima[t]  = 0
    label_prima[t] = 0

    pred = dict()
    succ = dict()
    pred[s]= None
    succ[t] = None

    while len(S & S_prima) == 0 :

        (u2add1, dist_min1) = d.popitem()
        label[u2add1] = dist_min1
        S.add(u2add1)
        for uvec in G.succesors(u2add1):

            if uvec not in S:  # si uvec no ha salido

                if d[uvec] > dist_min1 + l[(u2add1, uvec)]:
                    d[uvec] = dist_min1 + l[(u2add1, uvec)]
                    pred[uvec] = u2add1



        (u2add2, dist_min2) = d_prima.popitem()
        label_prima[u2add2] = dist_min2
        S_prima.add(u2add2)
        for uvec in G.predecessors(u2add2):


            if uvec not in S_prima: # si uvec no ha salido

                if  d_prima[uvec] > dist_min2 + l[(uvec,u2add2)]:
                    d_prima[uvec] = dist_min2 + l[(uvec,u2add2)]
                    succ[uvec] = u2add2


    label_total = dict()
    for vertice in G.vertices:
        label_total[vertice] = label[vertice] + label_prima[vertice]

    joint = min(label_total.keys(), key=lambda _: label_total[_])

    inicio , final = [], []

    inicio.append(joint)
    actual = joint
    while pred[actual] != None:
        inicio.append(pred[actual])
        actual = pred[actual]
    inicio.reverse()

    actual = joint
    while succ[actual] != None:
        final.append(succ[actual])
        actual = succ[actual]

    path = inicio + final

    print(path, label_total[joint])
    return path

### implementaciones ineficientes###
def pareto_set(A):
    """ Dado una lista de n duplas, encuentra el frente
        Pareto (para un problema de minimización)
        en O(nlog(n)), usando primero mergesort para ordenar
        las duplas en orden ascendente respecto a la primera coordenada
        (sin importar la segunda) y posteriormente busca las duplas
        eficientes comparando la segunda coordenada, haciendo un recorrido
        del frente de pareto como descendiendo en una escalera.

                :param A:
                :type A: dict of pairs (x,y)
                """
    # El Timsort inicial cuesta O(nlog(n)) y la búsqueda
    #posterior cuesta O(n). La complejidad es  O(n log(n)) + O(n)
    # o sea O(nlog(n)).

    A.sort(key=lambda x:x[0])
    pareto = list()
    (u,v) = A[0]
    pareto.append((u,v))
    actual = v

    for j in range(1,len(A)):
        if A[j][1] <= actual:
            pareto.append(A[j])
            actual = A[j][1]
        else:
            pass
    return pareto

def SPPTW_basic(G,s,time,costo,ventana):
    #P: crear un diccionario, donde cada clave es el entero que representa
    #un vértice del grafo y donde el valor es una lista que contiene
    #las etiquetas ya extendidas.

    # Q es un diccionario similar a P, donde las listas contienen las
    # etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"),float("inf"))] for vertice in G.vertices})
    P[s] = [(0, 0)]
    Q[s] = []
    actual = s
    efe_q = (0,0)
    QQ = [efe_q]

    while len(QQ)>0:

        # Definir una función que tome actual y efe_q y devuelva los nodos
        # a los cuales se puede extender efe_q desde actual.
        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual,vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual,vecino)])
                label_cost = efe_q[1] + costo[(actual,vecino)]
                #agregar la etiqueta (label_time, label_cost) a Q[vecino]
                #luego actualizar el frente de pareto de Q[vecino] usando Pareto_set.
                Q[vecino].append((label_time, label_cost))
                Q[vecino] = pareto_set(Q[vecino])
                # QQ es la unión de todos las listas que están como valores
                # del diccionario Q. Estas listas pueden cambiar mucho cuando se añade
                # una nueva etiqueta y se actualiza el frente de Pareto, QQ también puede
                # cambiar mucho.  Aqui optamos por crear un nuevo heap en cada iteración.

        QQ = list()
        for clave in Q.keys():
            for par in Q[clave]:
                QQ.append((par,clave)) # ((tiempo,costo),clave).

        # Sacamos el mínimo del heap QQ
        root = heapq.heappop(QQ)
        efe_q, actual = root[0], root[1]
        # root[0] nos es la etiquete mínima en el orden lexicográfico
        # root[1] nos dice el nodo al cual hay que actualizar Q[nodo] y P[nodo]
        P[actual].append(efe_q)
        Q[actual].remove(efe_q)

    return P

def SPPTW_basic_B(G,s,time,costo,ventana):
    #P: crear un diccionario, donde cada clave es el entero que representa
    #un vértice del grafo y donde el valor es una lista que contiene
    #las etiquetas ya extendidas.

    # Q es un diccionario similar a P, donde las listas contienen las
    # etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"),float("inf"))] for vertice in G.vertices})
    Q_set = dict({vertice:{ (float("inf"),float("inf")) }    for vertice in G.vertices} )
    P[s] = [(0, 0)]
    Q[s] = []
    Q_set[s] = set()
    actual = s
    efe_q = (0,0)
    QQ = list()
    for clave in Q.keys():
        for par in Q[clave]:
            QQ.append((par,clave))
    QQ_set = set(QQ)


    while len(QQ)>0:

        # Definir una función que tome actual y efe_q y devuelva los nodos
        # a los cuales se puede extender efe_q desde actual.
        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual,vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual,vecino)])
                label_cost = efe_q[1] + costo[(actual,vecino)]
                #agregar la etiqueta (label_time, label_cost) a Q[vecino]
                #luego actualizar el frente de pareto de Q[vecino] usando Pareto_set.
                Q_vecino2 = Q[vecino].copy()
                Q_vecino2.append((label_time, label_cost))
                Q_vecino2 = pareto_set(Q_vecino2)
                Q_vecino2_set = set(Q_vecino2)
                # contiene el frente de Pareto en el nodo vecino2
                print('Q_VECINO',Q[vecino])
                print('Q_VECINO2',Q_vecino2)
                for par in Q[vecino]:
                    print(par)
                    if par not in Q_vecino2_set:
                        QQ.remove((par,vecino))
                        QQ_set.remove((par,vecino))

                for par in Q_vecino2:
                    if par not in Q_set[vecino]:
                        heapq.heappush(QQ,(par,vecino))
                        QQ_set.add((par,vecino))
                Q[vecino] = Q_vecino2
                Q_set[vecino] = Q_vecino2_set

                # QQ es la unión de todos las listas que están como valores
                # del diccionario Q. Estas listas pueden cambiar mucho cuando se añade
                # una nueva etiqueta y se actualiza el frente de Pareto, QQ también puede
                # cambiar mucho. Aqui optamos por crear un heap al inicio y actualizar en cada
                # iteración.
                # Para verificar si un elemento está en el heap mantenemos un conjunto con
                # sus elementos.

        # Sacamos el mínimo del heap QQ
        root = heapq.heappop(QQ)
        print(root)
        QQ_set.remove(root)
        efe_q, actual = root[0], root[1]
        # root[0] nos es la etiquete mínima en el orden lexicográfico
        # root[1] nos dice el nodo al cual hay que actualizar Q[nodo] y P[nodo]
        P[actual].append(efe_q)
        Q[actual].remove(efe_q)
        Q_set[actual].remove(efe_q)

    return P

##################################################


### implementaciones siguiendo desrochers 1988 #######

def reduce_to_pareto_frontier(A):

    """ Dado una lista ORDENADA (Lex) de n duplas, encuentra el frente
        Pareto (para un problema de minimización)
        en O(n). Busca las duplas
        eficientes comparando la segunda coordenada, haciendo un recorrido
        del frente de pareto como descendiendo en una escalera.

                :param A:
                :type A: dict of pairs (x,y)
                """
    # La búsqueda cuesta O(n).


    pareto = list()
    (u, v) = A[0]
    pareto.append((u, v))
    actual = v

    for j in range(1, len(A)):
        if A[j][1] <= actual:
            pareto.append(A[j])
            actual = A[j][1]
        else:
            pass
    return pareto

def preserve_pareto_frontier(A,new_label):
    """ Dado una lista ordenada (bajo orden lexicográfico)
        de n etiquetas (tiempo, costo) eficientes, y una nueva etiqueta new_label
        verifica si ésta es eficiente y debe incluirse en A preservando el orden
        Lex, y elimina de A aquellas etiquetas que ahora resultan dominadas por
        new_label.

                :param A:
                :type A: dict of pairs (x,y)
                :param new_label:
                :type new_label: ordered pair (new_time, new_cost)
                """

    # Este algoritmo tiene complejidad O(n), donde n es la longitud de A.
    contador, comparacion = 0, True
    for i in range(len(A)):

        # si la nueva etiqueta es dominada por alguna etiqueta en A
        # entonces (por el orden Lex) nueva_etiqueta no puede dominar
        # a ninguna  y salimos del ciclo.
        if (A[i][0] < new_label[0] and A[i][1] < new_label[1] ):
            comparacion = False
            break

        # si la nueva etiqueta (new) domina a cierta etiqueta (b) en A, entonces
        # en caso de ser la primera que encontramos, reemplazamos b por new en A
        # manteniendo el orden Lex, si no es la primera eliminamos b de A.
        elif (new_label[0] < A[i][0] and new_label[1] < A[i][1]):
            contador += 1
            if contador == 1:
                A[i] = new_label
            else:
                del A[i]
            comparacion = False

        # no(b < nueva_etiqueta) and no(nueva_etiqueta<b)
        elif ((new_label[0] <= A[i][0]  or new_label[0] <= A[i][0] )
              and (A[i][0] <= new_label[0]  or A[i][1] <= new_label[1] )):
            pass
    if comparacion == True:
        # si la nueva etiqueta no domina y no es dominada por
        # ninguna etiqueta de A, entonces insertamos esta
        # nueva etiqueta manteniendo el orden Lex. bisect tiene
        # complejidad O(n).
        bisect.insort(A,new_label)


    return A

def contain_pareto_frontier(A,new_label):
    """ Dado una lista ordenada A (bajo orden lexicográfico)
        de n etiquetas (tiempo, costo) eficientes, y una nueva etiqueta new_label
        verifica si ésta domina a A[0], en cuyo caso se hace A[0] = new_label.
        A sigue teniendo todas las etiquetas eficientes y potencialmente algunas
        etiquetas no eficientes.

                   :param A:
                   :type A: dict of pairs (x,y)
                   :param new_label:
                   :type new_label: ordered pair (new_time, new_cost)
                   """


    insertado = False
    if (new_label[0] < A[0][0] and new_label[1] < A[0][1]):

        A[0] = new_label
        insertado = True
    elif ((new_label[0] <= A[0][0]  or new_label[0] <= A[0][0] )
              and (A[0][0] <= new_label[0]  or A[0][1] <= new_label[1] )):
        bisect.insort(A, new_label)
        insertado = True


    return A, insertado

def spptw_desrochers1988_imp1(G,s,time,costo,ventana):

    # En la implementación 1 cada Q_j es una lista ordenada (orden Lex)
    # y tras crear una nueva etiqueta en el nodo j, se anexa si es eficiente
    # y se eliminan todas las etiquetas en Q_j que ya no lo sean.

    # Paso 1: inicialización
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"),float("inf"))] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    actual, efe_q, detener = s, (0,0), 0

    # Paso 2: Extender efe_q, mantener estrictamente el frente de Pareto
    # en cada lista Q[j].

    while detener == 0:

        # Extender la etiqueta efe_q desde nodo actual. Una extensión
        # es factible si se respetan ventanas de tiempo.

        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual,vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual,vecino)])
                label_cost = efe_q[1] + costo[(actual,vecino)]
                new_label = (label_time, label_cost)
                print('new label',new_label)
                # Actualizar el frente de Pareto (sólo se dejan etiquetas eficientes)
                Q[vecino] = preserve_pareto_frontier(Q[vecino],new_label)

        # Como la etiqueta efe_q perteneciente al nodo "actual" ya fue extendida
        # (es decir, tratada) actualizamos las listas P[actual] y Q[actual]

        P[actual].append(efe_q)
        Q[actual].remove(efe_q)


        # Encontrar efe_q como el mínimo entre los primeros elementos
        # (o sea los mínimos en orden Lex) de cada Q[j].

        # el testigo detener es idéntico a 1 si todos los Q[j] son vacios,
        # en cuyo caso el algoritmo se detiene. Notar que no es necesario
        # crear una nueva lista con el mínimo de cada Q[j].

        efe_q  = (float("inf"),float("inf"))
        detener = 1
        for vertice in G.vertices:

            if len(Q[vertice])>0 :
                detener *= 0
                if Q[vertice][0] < efe_q:
                    efe_q = Q[vertice][0]
                    actual = vertice
            else:
                detener *= 1

    return P

def spptw_desrochers1988_imp2(G,s,time,costo,ventana):
    # En la implementación 2 cada Q_j es una lista ordenada (orden Lex)
    # y tras crear una nueva etiqueta en el nodo j, se anexa tras comparar únicamente
    # con el primer elemento de la lista Q_j, de modo que ésta siempre contiene
    # etiquetas eficientes y potencialmente algunas etiquetas no eficientes.

    # Paso 1: inicialización
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"),float("inf"))] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    actual, efe_q, detener = s, (0,0), 0

    # Paso 2: Extender efe_q, mantener estrictamente el frente de Pareto
    # en cada lista Q[j].

    while detener == 0:

        # Extender la etiqueta efe_q desde nodo actual. Una extensión
        # es factible si se respetan ventanas de tiempo.

        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual,vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual,vecino)])
                label_cost = efe_q[1] + costo[(actual,vecino)]
                new_label = (label_time, label_cost)
                print('new label',new_label)
                # Actualizar el frente de Pareto (potencialmente hay etiquetas no eficientes)
                Q[vecino], insertado = contain_pareto_frontier(Q[vecino],new_label)


        # Como la etiqueta efe_q perteneciente al nodo "actual" ya fue extendida
        # (es decir, tratada) actualizamos las listas P[actual] y Q[actual]

        P[actual].append(efe_q)
        Q[actual].remove(efe_q)


        # Encontrar efe_q como el mínimo entre los primeros elementos
        # (o sea los mínimos en orden Lex) de cada Q[j].

        # el testigo detener es idéntico a 1 si todos los Q[j] son vacios,
        # en cuyo caso el algoritmo se detiene. Notar que no es necesario
        # crear una nueva lista con el mínimo de cada Q[j].

        efe_q  = (float("inf"),float("inf"))
        detener = 1
        for vertice in G.vertices:

            if len(Q[vertice])>0 :
                detener *= 0
                if Q[vertice][0] < efe_q:
                    efe_q = Q[vertice][0]
                    actual = vertice
            else:
                detener *= 1
    # Paso 4: Como para cada nodo j, la lista  P_j puede tener etiquetas no
    # eficientes, reducimos la lista hasta quedar sólo con el frente de Pareto.
    # como las listas ya están ordenadas en orden Lex, el costo es O(D), donde D
    # es el número de posibles etiquetas. NO ENTIENDO POR QUÉ EL ARTÍCULO DICE
    # QUE ES O(d) con d la máxima amplitud de una ventana de tiempo.

    for vertice in G.vertices:
        P[vertice] = reduce_to_pareto_frontier(P[vertice])

    return P

def spptw_desrochers1988_imp3(G,s,time,costo,ventana):
    # En la implementación 3 cada Q_j es una lista ordenada (orden Lex)
    # y tras crear una nueva etiqueta en el nodo j, se anexa tras comparar únicamente
    # con el primer elemento de la lista Q_j, de modo que ésta siempre contiene
    # etiquetas eficientes y potencialmente algunas etiquetas no eficientes.
    # también se adiciona la nueva etiqueta en un heap, del cual se va
    # extrayendo el mínimo (efe_q) (y no nos preocupamos por
    # las etiquetas no eficientes porque son las últimas en ser extraídas del heap).

    # Paso 1: inicialización
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"), float("inf"))] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    label_heap = [((0,0),s)]

    # Paso 2: Extender efe_q, mantener estrictamente el frente de Pareto
    # en cada lista Q[j].

    while label_heap:

        (efe_q,actual) = heapq.heappop(label_heap)

        # Extender la etiqueta efe_q desde nodo actual. Una extensión
        # es factible si se respetan ventanas de tiempo.

        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual, vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual, vecino)])
                label_cost = efe_q[1] + costo[(actual, vecino)]
                new_label = (label_time, label_cost)
                print('new label', new_label)
                # Actualizar el frente de Pareto (potencialmente hay etiquetas no eficientes)
                Q[vecino], insertado = contain_pareto_frontier(Q[vecino], new_label)
                if insertado == True:
                    heapq.heappush(label_heap, (new_label,vecino))

        # Como la etiqueta efe_q perteneciente al nodo "actual" ya fue extendida
        # (es decir, tratada) actualizamos las listas P[actual] y Q[actual]

        P[actual].append(efe_q)
        Q[actual].remove(efe_q)


    # Paso 4: Como para cada nodo j, la lista  P_j puede tener etiquetas no
    # eficientes, reducimos la lista hasta quedar sólo con el frente de Pareto.
    # como las listas ya están ordenadas en orden Lex, el costo es O(D), donde D
    # es el número de posibles etiquetas. NO ENTIENDO POR QUÉ EL ARTÍCULO DICE
    # QUE ES O(d) con d la máxima amplitud de una ventana de tiempo.

    for vertice in G.vertices:
        P[vertice] = reduce_to_pareto_frontier(P[vertice])

    return P
