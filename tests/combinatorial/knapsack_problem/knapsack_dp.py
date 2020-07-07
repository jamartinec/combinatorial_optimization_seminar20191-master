# coding: utf8

#DP algorithm for KP:
"""Suponga ya se ha computado una solución óptima para el problema knapsack usando un
    subconjunto de items y todas las capacidades hasta c. Entonces se agrega un item a este
    subconjunto  y se verifica si la solución óptima debe ser actualizada o no. Para ello se
    computa el posible cambio de las soluciones óptimas para cada uno de los problemas con las
    distintas capacidades.
    Recursión de Bellman:  si d<wj, significa que hemos considerado una mochila muy pequeña
    para contener al item j, entonces la presencia del item j no afecta el valor de la solución
    óptima z_{j-1}(d). Si el item j cabe en la mochila, hay dos posibilidades: no se empaca en la
    mochila, dando lugar a la solución óptima z_{j-1}(d). O si se empaca en la mochila el valor
    de la misma aumenta p_j, pero la capacidad de la misma para ubicar los items 1 hasta j-1 disminuyó w_j, de modo que la solución
    óptima está dada por z_{j-1}(d-wj)"""

# Returns the maximum value that can be put in a knapsack of capacity d
def kp_recursive(d , w , p , n):

	# Base Case
	if n == 0 or d == 0 :
		return 0

	# Si un elemento que se agrega supera la capacidad, el óptimo se encontrará con j-1 elementos
	if (w[n-1] > d):
		return kp_recursive(d , w , p , n-1)

	# Devuelve el máximo de dos casos dependiendo de si el j-ésimo elemento se incluye o no
	else:
		return max(p[n-1] + kp_recursive(d-w[n-1] , w , p , n-1),
				kp_recursive(d , w , p , n-1))



def kp_dynamicp(d, w, p, n):

    """construimos una tabla (lista de listas) de programación dinámica, que contendrá el valor óptimo en su esquina
    inferior derecha. La tabla se inicializa en 0's. Cada fila corresponde al número de items del
    subproblema, y cada columna corresponde a la capacidad fijada para ese subproblema"""

    T = [[0 for i in range(d+1)] for j in range(n+1)]


    for j in range(n+1):
        for i in range(d+1):
            # caso base: primera fila y columna de la tabla son nulas
            if j==0 or i==0:
                T[j][i] = 0
            elif (w[j-1]<= i):
                T[j][i] = max(T[j - 1][i], p[j - 1] + T[j - 1][i - w[j - 1]])

            else:
                T[j][i] = T[j - 1][i]
    print(T)
    return T[n][d]







