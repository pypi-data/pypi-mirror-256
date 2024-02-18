"""
Capítulo 2. Resolución de ecuaciones algebraicas. Regula-Falsi
Módulo que provee de los métodos para el algoritmo de Regula-Falsi
"""

import pandas as pd


class ResultadoRegulaFalsi:
    """
    Clase auxiliar que permite modelar el estado del algoritmo de Regula-Falsi en cada iteración

    Contenido:
        a: extremo inferior del intervalo [a,b]
        b: extremo superior del intervalo [a,b]
        x: valor de x
        fx: valor de f(x)
        fa: valor de f(a)
        fb: valor de f(b)
        error: valor del error cometido en dicha iteración
        primera_iter: si es la primera iteración de algoritmo; se usa para obviar el error en la primera iteración
    """

    def __init__(self, a, b, x, fx, fa, fb, error, primera_iter):
        self.a = a
        self.b = b
        self.x = x
        self.fx = fx
        self.fa = fa
        self.fb = fb
        self.error = error
        self.primera_iter = primera_iter


def regula_falsi(f, a: float, b: float, tol: float):
    """
    Descripción:
    -----------------
    Implementación del algoritmo de Regula-Falsi para aproximar raíces

    Descripción e hipótesis del algoritmo:
    --------------------------------------
        Método iterativo de división de intervalos. El método consiste en aproximar la raíz de la
        ecuación como el punto de intersección del segmento AB con el eje x

        Las hipótesis son:

        - En [a,b] la ecuación posee raíz única

        - f(x) es continua en [a,b]

        - f(a)*f(b) < 0

    Parámetros:
    ----------------
        f: función f(x) a evaluar. Es una función lambda
        a: extremo inferior del intervalo [a,b]
        b: extremo superior del intervalo [a,b]
        tol: cota para el error absoluto

    Salida:
    --------------
        list[list | float]: El primer elemento ([0]) es el listado de ResultadoRegulaFalsi, el segundo elemento ([1]) es la raíz hallada

    Ejemplo:
    --------------
        >> import math

        >> f = lambda x : x**2 - math.e**x

        >> a = -1

        >> b = 0

        >> tol = 0.0005

        >> r = regula_falsi(f, a, b, tol)

        >> print('Raíz hallada con método de Regula Falsi: {:.7f}'.format(r[1]))

        Raíz hallada con método de Regula Falsi: -0.7034548

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
    primera_iter = True
    ultimo_x = 0
    x = 0.0
    condicion = True

    while condicion:
        f_a = f(a)
        f_b = f(b)

        x = a - (b - a) * f_a / (f_b - f_a)
        f_x = f(x)
        error = abs(x - ultimo_x)

        retorno[0].append(ResultadoRegulaFalsi(a, b, x, f_x, f_a, f_b, error, primera_iter))

        if f_a * f_x < 0:
            b = x
        elif f_a * f_x > 0:
            a = x

        ultimo_x = x
        condicion = error > tol
        primera_iter = False

    retorno.append(x)
    return retorno


def convertir_resultados_rf(lista_resultados_regula_falsi):
    """
    Descripción:
    -------------
    Permite procesar el resultado del algoritmo de Regula-Falsi en una tabla (DataFrame de pandas)

    Parámetros:
    -------------
        lista_resultados_regula_falsi: lista de iteraciones que modela la clase ResultadoRegulaFalsi

    Salida:
    -------------
        DataFrame: tabla con el resultado del algoritmo de Regula-Falsi de forma ordenada

    Ejemplo:
    ------------
        >> import math

        >> f = lambda x : x**2 - math.e**x

        >> a = -1

        >> b = 0

        >> tol = 0.0005

        >> r = regula_falsi(f, a, b, tol)



    :param lista_resultados_regula_falsi: lista de iteraciones que modela la clase ResultadoRegulaFalsi
    """
    lista = []
    for r in lista_resultados_regula_falsi:
        l = ['{:.7f}'.format(r.a), '{:.7f}'.format(r.x), '{:.7f}'.format(r.b), '{:.7f}'.format(r.fa),
             '{:.7f}'.format(r.fx), '{:.7f}'.format(r.fb)]
        if r.primera_iter:
            l.append('-------')
        else:
            l.append('{:.7f}'.format(r.error))
        lista.append(l)

    df = pd.DataFrame(data=lista, columns=['a', 'x', 'b', 'f(a)', 'f(x)', 'f(b)', 'Em(x)'])
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = 'Iteración'
    return df
