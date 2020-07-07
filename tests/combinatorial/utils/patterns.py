# coding: utf8
# Copyright: MathDecision


def query_from_set(s):
    """ Consulta un elemento arbitrario del conjunto s """
    if not s:
        raise ValueError
    else:
        w = None
        for _ in s:
            w = _
            break
    return w

def inv(e):
    """ Retorna la arista inversa de e """
    v, w = e
    return (w, v)



if __name__ == '__main__':
    import time
    s = set(range(1000000))
    start = time.time()
    for _ in range(1000000):
        query_from_set(s)
    print(time.time() - start)