"""
Capítulo 2. Resolución de ecuaciones algebraicas. Bisección
Módulo que provee de los métodos para el algoritmo de bisección
"""

import pandas as pd


class ResultadoBiseccion:
    """
    Clase auxiliar que permite modelar el estado del algoritmo de Bisección en cada iteración

    Contenido:
        a: extremo inferior del intervalo [a,b]
        b: extremo superior del intervalo [a,b]
        x: valor de x
        fx: valor de f(x)
        fa: valor de f(a)
        fb: valor de f(b)
        error: valor del error cometido en dicha iteración
    """

    def __init__(self, a, b, x, fx, fa, fb, error):
        self.a = a
        self.b = b
        self.x = x
        self.fx = fx
        self.fa = fa
        self.fb = fb
        self.error = error


def biseccion(f, a: float, b: float, tol: float):
    """
    Descripción:
    -----------------
        Implementación del algoritmo de bisección para aproximar raíces en un intervalo dado

    Descripción e hipótesis del algoritmo:
    ---------------------------------------
        Método iterativo de división de intervalos. El método consiste en aproximar la raíz de la
        ecuación como el punto intermedio del intervalo [a,b].

        Las hipótesis son:

        - En [a,b] la ecuación posee raíz única

        - f(x) es continua en [a,b]

        - f(a)*f(b) < 0

    Parámetros:
    ---------------------------------------
        f: función f(x) a evaluar. Es una función lambda

        a: extremo inferior del intervalo [a,b]

        b: extremo superior del intervalo [a,b]

        tol: cota para el error absoluto

    Salida:
    ---------------------
        list[list | float]: El primer elemento ([0]) es el listado de ResultadoBiseccion, el segundo elemento ([1]) es la raíz hallada

    Ejemplo:
    -------------
        >> import math

        >> f = lambda x : x**2 - math.e**x

        >> a = -1

        >> b = 0

        >> tol = 0.0005

        >> r = biseccion(f, a, b, tol)

        >> print('Raíz hallada con método de Bisección: {:.7f}'.format(r[1]))

        Raíz hallada con método de Bisección: -0.7036133

    :param f: función f(x) a evaluar. Es una función lambda
    :param a: extremo inferior del intervalo [a,b]
    :param b: extremo superior del intervalo [a,b]
    :param tol: cota para el error absoluto
    """

    if a > b:
        raise ValueError("Intervalo mal definido")
    if f(a) * f(b) >= 0.0:
        raise ValueError("La función debe cambiar de signo en el intervalo")
    if tol <= 0:
        raise ValueError("La cota de error debe ser un número positivo")

    retorno = [[]]
    mitad = (a + b) / 2
    condicion = True

    while condicion:
        f_a = f(a)
        f_b = f(b)
        f_mitad = f(mitad)
        error = (b - a) / 2

        retorno[0].append(ResultadoBiseccion(a, b, mitad, f_mitad, f_a, f_b, error))

        if error < tol:
            retorno.append(mitad)
            condicion = False
        elif f_a * f_mitad > 0:
            a = mitad
        elif f_a * f_mitad < 0:
            b = mitad
        mitad = (a + b) / 2

    return retorno


def convertir_resultados_biseccion(lista_resultados_biseccion):
    """
    Descripcion:
    -----------------
        Permite procesar el resultado del algoritmo de bisección en una tabla (DataFrame de pandas)

    Parámetros:
    -----------------
        lista_resultados_biseccion: lista de iteraciones que modela la clase ResultadoBiseccion

    Salida:
    -----------------
        DataFrame: tabla con el resultado del algoritmo de bisección de forma ordenada

    Ejemplo:
    -----------------
        >> import math

        >> f = lambda x : x**2 - math.e**x

        >> a = -1

        >> b = 0

        >> tol = 0.0005

        >> r = biseccion(f, a, b, tol)

        >> dataframe = convertir_resultados_biseccion(r[0])

        >> print(tabulate(dataframe, headers="keys", tablefmt="fancy_grid"))

    :param lista_resultados_biseccion: lista de iteraciones que modela la clase ResultadoBiseccion
    """

    lista = []
    for r in lista_resultados_biseccion:
        lista.append(['{:.7f}'.format(r.a), '{:.7f}'.format(r.x), '{:.7f}'.format(r.b), '{:.7f}'.format(r.fa),
                      '{:.7f}'.format(r.fx), '{:.7f}'.format(r.fb), '{:.7f}'.format(r.error)])

    df = pd.DataFrame(data=lista, columns=['a', 'x', 'b', 'f(a)', 'f(x)', 'f(b)', 'Em(x)'])
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = 'Iteración'
    return df
