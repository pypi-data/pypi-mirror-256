"""
Capítulo 2. Resolución de ecuaciones algebraicas. Secantes
Módulo que provee de los métodos para el algoritmo de Secantes
"""

import pandas as pd


class ResultadoSecantes:
    """
    Clase que permite modelar el estado del algoritmo de Secantes en cada iteración

    Contenido:
        x: valor de x
        fx: valor de f(x)
        error: valor del error cometido en dicha iteración
        primera_iter: si es la primera iteración de algoritmo; se usa para obviar el error en la primera iteración
    """

    def __init__(self, x, fx, error, primera_iter):
        self.x = x
        self.fx = fx
        self.error = error
        self.primera_iter = primera_iter


def secantes(f, x0, x1, tol):
    """
    Implementación del algoritmo de Secantes para aproximar raíces

    Hipótesis del algoritmo:
        - En [a,b] la ecuación posee raíz única
        - f(x) es continua en [a,b]
        - f(a)*f(b) < 0
        - f'(x) y f''(x) son continuas y no nulas en [a,b]

    Parámetros:
        f: función f(x) a evaluar. Es una función lambda
        x0: define uno de los extremos x0 del intervalo
        x1: define uno de los extremos x1 del intervalo
        tol: cota para el error absoluto

    Salida:
        list[list | float]: El primer elemento ([0]) es el listado de ResultadoSecantes, el segundo elemento ([1]) es la raíz hallada

        """
    if f(x0) * f(x1) >= 0.0:
        raise ValueError("La función debe cambiar de signo en el intervalo")
    if tol <= 0:
        raise ValueError("La cota de error debe ser un número positivo")

    f_x0 = f(x0)
    f_x1 = f(x1)
    error = tol + 1
    xr = 0.0
    retorno = [[]]
    retorno[0].append(ResultadoSecantes(x0, f_x0, 0, True))
    retorno[0].append(ResultadoSecantes(x1, f_x1, 0, True))

    while error > tol:
        xr = x1 - ((x1 - x0) / (f_x1 - f_x0)) * f_x1
        f_xr = f(xr)
        error = abs(xr - x1)
        retorno[0].append(ResultadoSecantes(xr, f_xr, error, False))

        x0 = x1
        f_x0 = f(x0)
        x1 = xr
        f_x1 = f(x1)

    retorno.append(xr)
    return retorno


def convertir_resultados_secantes(lista_resultados_secantes):
    """
    Permite procesar el resultado del algoritmo de Secantes en una tabla (DataFrame de pandas)

    Parámetros:
        lista_resultados_secantes: lista de iteraciones que modela la clase ResultadoSecantes

    Salida:
        DataFrame: tabla con el resultado del algoritmo de Secantes de forma ordenada
    """
    lista = []
    for r in lista_resultados_secantes:
        l = ['{:.7f}'.format(r.x), '{:.7f}'.format(r.fx)]
        if r.primera_iter:
            l.append('---------')
        else:
            l.append('{:.7f}'.format(r.error))
        lista.append(l)

    df = pd.DataFrame(data=lista, columns=['xi', 'f(x)', 'Em(x)'])
    df.index.name = 'Iteración'
    return df
