"""
Capítulo 2. Separación de raíces.
Módulo que provee de los principales algoritmos de separación de raíces:
- Teorema de Bolzano-Cauchy
- Teorema de Descartes
- Teorema de Lagrange
- Método Gráfico
"""
from core.auxiliares.auxiliares import (coeficientes_polinomio, intervalo_negativo, aux_descartes,
                                        aux_lagrange)
from sympy.plotting import plot


def descartes(f):
    """
    Descripción:
    ----------------
        Permite conocer la cantidad de cambios de signo m de la función f tanto en el intervalo positivo, como
        en el negativo.

    Implementación:
    -----------------
        La implementación devuelve 2 valores de m, tanto raíces positivas como negativas. Dicho valor
        es el número de cambios de signo en la sucesión de coeficientes. El número de raíces, tanto
        positivas como negativas se determina según su paridad:

        .m=0 -> 0

        .m=1 -> 1

        .m=2 -> 0 ó 2

        .m=3 -> 1 ó 3

        .m=4 -> 0 ó 2 ó 4

        .m=5 -> 1 ó 3 ó 5

        ...

    Parámetros:
    ----------------
        f: Función string

    Salida:
    ----------------
        tuple[int, int]: Cantidad de cambios de signo m en el intervalo positivo y negativo

    Ejemplo:
    ----------------
        >> f = "4x^3-6x^2+1"

        >> pos_interval, neg_interval = descartes(f)

        >> print(f'Descartes aplicado en intervalo positivo -> m={pos_interval}')

        Descartes aplicado en intervalo positivo -> m=2

        >> print(f'Descartes aplicado en intervalo negativo -> m={neg_interval[0]}')

        Descartes aplicado en intervalo negativo -> m=1

    :param f: Función string
    """
    valores = coeficientes_polinomio(f)
    result_pos = aux_descartes(valores)
    result_neg = aux_descartes(intervalo_negativo(valores))

    return ([i for i in range(result_pos, 0, -2)][0]), ([i for i in range(result_neg, 0, -2)][0])


def cantidad_raices_descartes(m: int):
    """
    Descripción:
    ----------------
        Permite conocer la cantidad de raíces posibles según m dado.

    Parámetros:
    ----------------
        m: Número de cambios de signos resultante de la aplicación del método de descartes

    Salida:
    ----------------
        list[int]: Cantidad de raíces posibles

    Ejemplo:
    ----------------
        >> f = "4x^3-6x^2+1"

        >> pos_interval, neg_interval = descartes(f)

        >> cant_raices_positivas, cant_raices_negativas = cantidad_raices_descartes(pos_interval), cantidad_raices_descartes(neg_interval)

        >> print(f'La cantidad posible de raíces positivas es: {" ó ".join([str(x) for x in cant_raices_positivas])}')

        La cantidad posible de raíces positivas es: 0 ó 2

        >> print(f'La cantidad posible de raíces negativas es: {" ó ".join([str(x) for x in cant_raices_negativas])}')

        La cantidad posible de raíces negativas es: 1

    :param m: Número de cambios de signos resultante de la aplicación del método de descartes
    """
    cant_raices = []

    for x in range(0 if m % 2 == 0 else 1, m + 2, 2):
        cant_raices.append(x)

    return cant_raices


def bolzano_cauchy(f, a: float, b: float):
    """
    Descripción:
    --------------
    Permite conocer si la función f en el intervalo [a, b] tiene al menos una raíz

    Parámetros:
    ---------------
        f: Función lambda f(x) de la ecuación en la forma f(x)=0

        a: Extremo inferior del intervalo [a, b]

        b: Extremo superior del intervalo [a, b]

    Salida:
    ---------------
        bool: Si la función tiene al menos una raíz en el intervalo dado

    Ejemplo:
    ---------------
        >> import math

        >> f = lambda x: (math.e**-x)-x

        >> a = 0

        >> b = 1

        >> r = 'Tiene' if bolzano_cauchy(f, a, b) else 'No tiene'

        >> print(f'{r} al menos una raíz')

        Tiene al menos una raíz

    :param f: Función lambda f(x) de la ecuación en la forma f(x)=0
    :param a: Extremo inferior del intervalo [a, b]
    :param b: Extremo superior del intervalo [a, b]
    """
    return f(a) * f(b) < 0


def lagrange(f):
    """
    Descripción:
    ----------------
        Permite hallar una aproximación de los intervalos de las raíces positivas y negativas.

    Parámetros:
    ----------------
        f: Función string

    Salida:
    ----------------
        tuple[float, float]: Aproximación del intervalo de la raíz en el los intervalos positivos y negativos
        respectivamente

    Ejemplo:
    ----------------
        >> f = "4x^3-6x^2+1"

        >> pos_interval, neg_interval = lagrange(f)

        >> print('Lagrange aplicado en intervalo positivo: [0, {}]'.format(pos_interval) )

        Lagrange aplicado en intervalo positivo: [0, 2.5]

        >> print('Lagrange aplicado en intervalo negativo: [-{}, 0]'.format(neg_interval) )

        Lagrange aplicado en intervalo negativo: [-1.6299605249474367, 0]

    :param f: Función string
    """
    valores = coeficientes_polinomio(f)
    result_neg = aux_lagrange(intervalo_negativo(valores))
    result_pos = aux_lagrange(valores)

    return result_pos, result_neg


def metodo_grafico(symbol, a: float, b: float, f1, f2=None):
    """
    Descripción:
    ----------------
        Permite determinar las raíces de una ecuación algebraica o transcendente de forma visual
        gracias a su representación gráfica

    Versión 1:
    ---------------
        Se emplea solamente una función (f1).
        Procedimiento:

        - Transformar la ecuación a la forma f(x) = 0

        - Tomar f(x) como f1

        - Elegir un intervalo primario [a, b] (Ej: [-5, 5]) para reconocer las raíces de la ecuación, que son donde la función graficada corta el eje x

        - Disminuir el intervalo dado para determinar el rango de cada raíz de la ecuación

    Versión 2:
    ---------------
        Se emplean 2 funciones (f1 y f2).
        Procedimiento:

        - Transformar la ecuación a la forma f1(x) = f2(x)

        - Tomar f1(x) como f1 y f2(x) como f2

        - Elegir un intervalo primario [a, b] (Ej: [-5, 5]) para reconocer las raíces de la ecuación, que son donde ambas funciones se cortan

        - Disminuir el intervalo dado para determinar el rango de cada raíz de la ecuación

    Parámetros:
    ----------------
        symbol: Símbolo de sympy usado en la/las funciones pasadas

        a: Extremo superior del intervalo [a,b]

        b: Extremo inferior del intervalo [a,b]

        f1: Función sympy

        f2: Función sympy opcional en dependencia de la versión usada

    Salida:
    ----------------
        Plot: Plot de Sympy. Si se captura en un Jupyter Notebook o en SciView, no es necesario
        trabajar con él, pues se guarda automáticamente el resultado en forma de imagen. En
        otro contexto se podría utilizar el método .show() para ver el resultado

    Ejemplo:
    ----------------
        Versión 1

        >> from sympy import symbols

        >> import math

        >> x = symbols('x')

        >> f1 = (math.e ** -x) - x

        >> a = 0

        >> b = 1

        >> metodo_grafico(x, a, b, f1)



        Versión 2

        >> from sympy import symbols

        >> import math

        >> x = symbols('x')

        >> f1 = math.e ** -x

        >> f2 = x

        >> a = 0

        >> b = 1

        >> metodo_grafico(x, a, b, f1, f2)

    :param symbol: Símbolo de sympy usado en la/las funciones pasadas
    :param a: Extremo superior del intervalo [a,b]
    :param b: Extremo inferior del intervalo [a,b]
    :param f1: Función sympy
    :param f2: Función sympy opcional en dependencia de la versión usada
    """
    if f2 is None:
        return plot(f1, (symbol, a, b))
    else:
        return plot(f1, f2, (symbol, a, b))
