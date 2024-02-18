"""
Métodos Auxiliares
Módulo que provee de métodos auxiliares y utilidades necesarios en otros módulos
"""
import math
import re


def coeficientes_polinomio(polinomio):
    regexp = r"(-?\d*)(x?)(?:(?:\^|\*\*)(\d))?"
    c = {}

    for coef, x, exp in re.findall(regexp, polinomio):
        if not coef and not x:
            continue
        if x and not coef:
            coef = '1'
        if x and coef == "-":
            coef = "-1"
        if x and not exp:
            exp = '1'
        if coef and not x:
            exp = '0'

        try:
            c[int(exp)] = c[int(exp)] + float(coef)
        except KeyError:
            c[int(exp)] = float(coef)

    grado = max(c)
    coeficientes = [0.0] * (grado + 1)

    for g, v in c.items():
        coeficientes[g] = v
    coeficientes.reverse()

    if coeficientes[0] < 0:
        coeficientes = max_grado_positivo(coeficientes)

    return coeficientes


def max_grado_positivo(valores):
    coeficientes = [i * (-1) for i in valores]
    return coeficientes


def intervalo_negativo(valores):
    resultado = list.copy(valores)

    if len(valores) % 2 == 0:  # si tiene una cantidad par de coeficientes significa que el grado es impar
        i = 0
        resultado = max_grado_positivo(valores)
    else:
        i = 1

    for v in range(i, len(resultado) - 1, 2):
        resultado[v] = resultado[v] * (-1)

    return resultado


def aux_descartes(valores):
    valor = valores[0]
    contador = 0

    for n in valores[1:]:
        if valor * n < 0:
            valor = n
            contador = contador + 1

    return contador


def encontrar_k(valores):
    for i in range(len(valores)):
        if valores[i] < 0:
            return i


def aux_lagrange(valores):
    b = min(valores)

    if b > 0:
        raise Exception('No existen coeficientes negativos')

    b = abs(b)
    k = encontrar_k(valores)

    if k is None:
        raise Exception('No existen coeficientes negativos')

    return 1 + math.pow(b / valores[0], 1 / k)
