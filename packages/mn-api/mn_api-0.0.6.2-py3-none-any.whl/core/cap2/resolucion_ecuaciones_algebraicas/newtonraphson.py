"""
Capítulo 2. Resolución de ecuaciones algebraicas. Newton-Raphson
Módulo que provee de los métodos para el algoritmo de Newton-Raphson
"""

import pandas as pd
from sympy import lambdify, diff
from sympy.abc import x


class ResultadoNewtonRaphson:
    """
    Clase auxiliar que permite modelar el estado del algoritmo de Newton-Raphson en cada iteración

    Contenido:
        x: valor de x
        fx: valor de f(x)
        dxfx: valor de f'(x)
        error: valor del error cometido en dicha iteración
        primera_iter: si es la primera iteración de algoritmo; se usa para obviar el error en la primera iteración
    """

    def __init__(self, x, fx, dxfx, error, primera_iter):
        self.x = x
        self.fx = fx
        self.dxfx = dxfx
        self.error = error
        self.primera_iter = primera_iter


def newton_raphson(f, x_0: float, tol: float):
    """
    Descripción:
    ---------------
        Implementación del algoritmo de Newton-Raphson para aproximar raíces

    Descripción e hipótesis del algoritmo:
    ----------------------------------------
        Método iterativo de puntos. El método consiste en aproximar la raíz de la ecuación como el
        punto de intersección con el eje x, de la recta tangente a la función x0.

        Las hipótesis son:

        - En [a,b] la ecuación posee raíz única

        - f(x) es continua en [a,b]

        - f(a)*f(b) < 0

        - f'(x) y f''(x) son continuas y no nulas en [a,b]

        - x0 que pertenece al intervalo [a,b], cumple que f(x0)*f''(x0) > 0

    Parámetros:
    ----------------
        f: función f(x) a evaluar. Es una función simbólica de sympy usando la x simbólica

        x_0: define el punto de partida x0 del método

        tol: cota para el error absoluto

    Salida:
    ------------
        list[list | float]: El primer elemento ([0]) es el listado de ResultadoNewtonRaphson, el segundo elemento ([1]) es la raíz hallada

    Ejemplo:
    -------------
        >> from sympy.abc import x

        >> f = x*exp(x)-2

        >> x0 = 1

        >> tol = 0.0005

        >> r = newton_raphson(f, x0, tol)

        >> print('Raíz hallada con método de Newton-Raphson: {:.7f}'.format(r[1]))

        Raíz hallada con método de Newton-Raphson: 0.8526055

    :param f: función f(x) a evaluar. Es una función simbólica de sympy usando la x simbólica
    :param x_0: define el punto de partida x0 del método
    :param tol: cota para el error absoluto
    """

    x_anterior = x_0
    condition = True
    x_r = 0.0
    f1 = lambdify(x, f)
    f_dx = lambdify(x, diff(f, x))
    f = f1
    retorno = [[ResultadoNewtonRaphson(x_0, f(x_0), f_dx(x_0), 0, True)]]

    while condition:
        x_r = x_anterior - f(x_anterior) / f_dx(x_anterior)
        error = abs(x_r - x_anterior)

        retorno[0].append(ResultadoNewtonRaphson(x_r, f(x_r), f_dx(x_r), error, False))
        x_anterior = x_r
        condition = error > tol

    retorno.append(x_r)
    return retorno


def convertir_resultados_nr(lista_resultados_nr):
    """
    Descripción:
    ----------------
        Permite procesar el resultado del algoritmo de Newton-Raphson en una tabla (DataFrame de pandas)

    Parámetros:
    ----------------
        lista_resultados_nr: lista de iteraciones que modela la clase ResultadoNewtonRaphson

    Salida:
    ----------------
        DataFrame: tabla con el resultado del algoritmo de Newton-Raphson de forma ordenada
        
    Ejemplo:
    -----------------
        >> from sympy.abc import x

        >> f = x*exp(x)-2

        >> x0 = 1

        >> tol = 0.0005

        >> r = newton_raphson(f, x0, tol)
        
        >> dataframe = convertir_resultados_nr(r[0])

        >> print(tabulate(dataframe, headers="keys", tablefmt="fancy_grid"))
        
    :param lista_resultados_nr: lista de iteraciones que modela la clase ResultadoNewtonRaphson
    """

    lista = []
    for r in lista_resultados_nr:
        l = ['{:.7f}'.format(r.x), '{:.7f}'.format(r.fx), '{:.7f}'.format(r.dxfx)]
        if r.primera_iter:
            l.append('---------')
        else:
            l.append('{:.7f}'.format(r.error))
        lista.append(l)

    df = pd.DataFrame(data=lista, columns=['xi', 'f(x)', 'f\'(x)', 'Em(x)'])
    df.index.name = 'Iteración'
    return df
