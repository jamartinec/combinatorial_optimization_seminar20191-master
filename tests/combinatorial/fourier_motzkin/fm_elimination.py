# coding: utf8
import numpy as np


def reducir(a):
    u, v = a.shape
    arreglo = list()
    arreglo.append(a)
    for j in range(v - 1, 0, -1):
        I0 = list()
        Ipo = list()
        Ine = list()
        u, v = a.shape
        for i in range(u):
            a[i, :] = a[i, :].astype('float')
            d = a[i, j - 1]
            d = d.astype('float')

            if d == 0:
                I0.append(i)
            elif d > 0:
                Ipo.append(i)
                a[i, :] = a[i, :] / d
            else:
                Ine.append(i)
                a[i, :] = a[i, :] / -d

        if (len(Ipo) == 0 or len(Ine) == 0):
            arreglo.append(a)
            pass

        else:
            l = list()
            for i in Ipo:
                l.append(i)
                for j in Ine:
                    l.append(j)
                    b = a[i, :] + a[j, :]
                    a = np.vstack([a, b])
            a = np.delete(a, l, axis=0)
            arreglo.append(a)

    E = set(np.nonzero(np.any(a != 0, axis=0))[0])
    E.remove(v - 1)

    M = list()
    m = list()
    for e in list(E):
        for i in range(u):
            if a[i, e] > 0:
                M.append(a[i, v - 1] / a[i, e])
            elif a[i, e] < 0:
                m.append(a[i, v - 1] / a[i, e])
            else:
                pass
        break
    # estándar desigualdades <=
    print('M', M)
    print('m', m)

    if len(M) == 0 and len(m) == 0:
        if np.any(a[:, v - 1] < 0, axis=0):
            print('infactible')  # retornar status infactible para el sistema
        else:
            t = 1
    elif len(M) != 0 and len(m) == 0:
        t = min(M)
    elif len(M) == 0 and len(m) != 0:
        t = max(m)
    else:
        t = (min(m) + max(M)) / 2
    print('arreglo', arreglo)
    return arreglo


def despejar(a):
    u, v = a.shape
    E = list(np.nonzero(np.any(a != 0, axis=0))[0])
    E.sort()
    if len(E) == 1:

        e = E[0]
        t=None
        if np.any(a[:, v - 1] < 0, axis=0):
            print('infactible')  # retornar status infactible para el sistema
            # debería terminar el programa acá
        else:
            print('factible')
            t = None


    elif len(E) >= 2:
        e = E[-2]  # Toma el penúltimo índice de columnas no nulas
        print('type e', type(e))
        M = list()
        m = list()
        for i in range(u):
            if a[i, e] > 0:
                M.append(a[i, v - 1] / a[i, e])
            elif a[i, e] < 0:
                m.append(a[i, v - 1] / a[i, e])
            else:
                pass

        if len(M) != 0 and len(m) == 0:
            t = min(M)
        elif len(M) == 0 and len(m) != 0:
            t = max(m)
        elif len(M) != 0 and len(m) != 0:
            t = (min(m) + max(M)) / 2

    return (e, t)


def sustitucion(arreglo):
    j = len(arreglo) - 1
    actual = arreglo[j]
    print('actual', actual)
    dicci = dict()
    while j >= 1:
        (e, t) = despejar(actual)
        dicci[e] = t
        anterior = arreglo[j - 1]
        actual = eliminar(anterior, dicci)
        j = j - 1
    (e, t) = despejar(actual)
    dicci[e] = t
    return dicci


def eliminar(b, dicci):
    u, v = b.shape
    for e in dicci.keys():
        if dicci[e] != None:
            b[:, e] *= dicci[e]
            b[:, v - 1] = b[:, v - 1] - b[:, e]
            b[:, e] = 0
        else:
            pass
    return b


def f_m(a):
    arreglo = reducir(a)
    dicci = sustitucion(arreglo)
    return dicci

