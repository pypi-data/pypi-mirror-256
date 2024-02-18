"""
Capítulo 1. Medidas del error.
Módulo que provee de los principales algoritmos de medidas del error:
- Error
- Error absoluto
- Error relativo
- Mínimo error absoluto máximo
"""


def error(x: float, xa: float):
    """
    Descripción:
    ---------------
        Permite calcular el error del valor aproximado con respecto al valor exacto

    Parámetros:
    ---------------
        x: valor exacto

        xa: valor aproximado

    Salida:
    ----------------
        float: error del valor aproximado en relación con el valor exacto

    Ejemplo:
    ----------------
        >> x = 10.2

        >> xa = 11.9

        >> print(f'El error es {error(x,xa)}')

        El error es -1.700000000000001

    :param x: valor exacto
    :param xa: valor aproximado
    """

    return x - xa


def error_abs(error: float) -> float:
    """
    Descripción:
    --------------
        Permite calcular el error absoluto E(x) dado el error

    Parámetros:
    --------------
        error: error del valor aproximado xa

    Salida:
    ---------------
        float: error absoluto

    Ejemplo:
    --------------
        >> error = -0.9

        >> print(f'El error absoluto es {error_abs(error)}')

        El error absoluto es 0.9

    :param error: error del valor aproximado xa
    """

    return abs(error)


def error_rel(error_abs: float, x: float):
    """
    Descripción:
    ---------------
        Permite calcular el error relativo e(x) dado el error absoluto y el valor exacto

    Parámetros:
    ---------------
        error_abs: error absoluto

        x: valor exacto

    Salida:
    ---------------
        float: error relativo

    Ejemplo:
    ---------------
        >> error_abs = 0.9

        >> x = 12.2

        >> print(f'El error relativo es {error_rel(error_abs, x)}')

        El error relativo es 0.0737704918032787

    :param error_abs: error absoluto
    :param x: valor exacto
    """

    return error_abs / abs(x)


def min_error_abs_max(a: float, b: float):
    """
    Descripción:
    ---------------
        Permite obtener el mínimo error absoluto máximo Em(x) en el intervalo [a,b]

    Parámetros:
    ---------------
        a: punto inicial del intervalo [a,b]

        b: punto final del intervalo [a,b]

    Salida:
    ---------------
        float: mínimo error absoluto máximo

    Ejemplo:
    ---------------
        >> a = 6.23

        >> b = 9.67

        >> print(f'El mínimo error absoluto máximo en el intervalo [{a}, {b}], es {min_error_abs_max(a, b)}')

        El mínimo error absoluto máximo en el intervalo [6.23, 9.67], es 7.95

    :param a: punto inicial del intervalo [a,b]
    :param b: punto final del intervalo [a,b]
    """

    return (a + b) / 2
