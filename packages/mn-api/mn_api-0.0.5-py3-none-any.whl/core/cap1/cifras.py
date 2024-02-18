"""
Capítulo 1. Cifras significativas, decimales y exactas.
Módulo que provee de los principales métodos para el cálculo de:
- Cifras decimales
- Cifras significativas
- Cifras exactas
"""
import pandas as pd


def cifras_sig(x: float | str):
    """
    Descripción:
    ---------------
        Permite contar la cantidad de cifras significativas de un valor x

    Parámetros:
    ---------------
        x: valor x a procesar

    Salida:
    ---------------
        int: cantidad de cifras significativas

    Ejemplo:
    ---------------
        >> x = '0.002030'

        >> print(f'Tiene {cifras_sig(x)} cifras significativas')

        Tiene 4 cifras significativas

    :param x: valor x a procesar
    """

    a = str(x)
    cont = 0
    if float(x) >= 1:
        cont = len(str(x))
        if a.count('.') == 1 or a.count(',') == 1:
            cont -= 1
        return cont

    contar1 = False
    contar2 = False
    for i in a:
        if i != '0' and i != ',' and i != '.':
            contar1 = True
        if contar1 and contar2:
            cont += 1
        if i == ',' or i == '.':
            contar2 = True
    return cont


def cifras_dec(x: float | str):
    """
    Descripción:
    ---------------
        Permite contar la cantidad de cifras decimales de un valor x

    Parámetros:
    ---------------
        x: valor x a procesar

    Salida:
    ---------------
        int: cantidad de cifras decimales

    Ejemplo:
    ---------------
        >> x = '12.3344'

        >> print(f'Tiene {cifras_dec(x)} cifras decimales')

        Tiene 4 cifras decimales

    :param x: valor x a procesar
    """

    a = str(x)
    cont = 0
    contar = False
    for i in a:
        if contar:
            cont += 1
        if i == '.' or i == ',':
            contar = True
    return cont


class ResultadoCifrasExactas:
    """
    Clase que permite modelar los resultados del método para hallar las cifras exactas

    Contenido:
        lista_filas_proc: contiene la lista con los estados en cada iteración del algoritmo de las cifras exactas
        valor_cifras_exactas: valor que contiene las cifras exactas del número original.
    """

    def __init__(self, lista, valor):
        self.lista_filas_proc = lista
        self.valor_cifras_exactas = valor


class FilaProcCifrasExactas:
    """
    Clase que permite modelar el estado de cada iteración del algoritmo de las cifras exactas

    Contenido:
        digito: cifra o dígito a analizar en la iteración
        pos_k: k-ésima posición (acorde al valor posicional del dígito)
        valor_pos: valor posicional del dígito analizado en la iteración
        dig_exacto: booleano que determina si un dígito es exacto o no
    """

    def __init__(self, dig, pos, valor, dig_exacto):
        self.digito = dig
        self.pos_k = pos
        self.valor_pos = valor
        self.dig_exacto = dig_exacto


def cifras_exactas(xa: float | str, error_abs: float):
    """
    Descripción:
    --------------
        Permite procesar la cantidad de cifras exactas de un valor dados su valor aproximado y el error absoluto

    Parámetros:
    -------------
        xa: valor aproximado xa (x*)

        error_abs: error absoluto E(x)

    Salida:
    -------------
        ResultadoCifrasExactas: resultado del algoritmo de cifras exactas

    Ejemplo:
    ------------
        >> xa = 3.1415

        >> error_abs = 0.0002

        >> r = cifras_exactas(xa, error_abs)

        >> print('El valor exacto es: '+str(r.valor_cifras_exactas))

        El valor exacto es: 3.141

    :param xa: valor aproximado xa (x*)
    :param error_abs: error absoluto E(x)
    """

    cont = 0
    lista = []
    parar = False
    for i in str(xa):
        if i != '.' and i != ',':
            cont += 1
        else:
            break

    pos = cont - 1
    j = 0
    comp = False
    exacta = False
    valor_exacto = ''

    while not parar and j < len(str(xa)):
        cifra = str(xa)[j]
        if cifra != '.' and cifra != ',':
            p = pos
            c = cifra
            v = 0.5 * pow(10, pos)
            comp = error_abs <= 0.5 * pow(10, pos)
            pos -= 1
            if not comp:
                parar = True
                exacta = False
            else:
                exacta = True
            lista.append(FilaProcCifrasExactas(c, p, v, exacta))
        if exacta:
            valor_exacto += str(cifra)
        j += 1

    return ResultadoCifrasExactas(lista, valor_exacto)


def convertir_resultados_cifras_exactas(lista_resultados_cifras_exactas):
    """
    Descripción:
    -----------------
        Permite procesar el resultado del algoritmo de las cifras exactas en una tabla (DataFrame de pandas)

    Parámetros:
    -----------------
        lista_resultados_cifras_exactas: lista de iteraciones que se encuentra en la clase ResultadoCifrasExactas

    Salida:
    -------------------
        DataFrame: tabla con el resultado del algoritmo de las cifras exactas de forma ordenada

    Ejemplo:
    -------------------
        >> xa = 3.1415

        >> error_abs = 0.0002

        >> r = cifras_exactas(xa, error_abs)

        >> print(convertir_resultados_cifras_exactas(r.lista_filas_proc))

        >> dataframe = convertir_resultados_cifras_exactas(r.lista_filas_proc)

        >> print(tabulate(dataframe, headers="keys", tablefmt="fancy_grid"))

    :param lista_resultados_cifras_exactas: lista de iteraciones que se encuentra en la clase ResultadoCifrasExactas
    """

    lista = []
    for r in lista_resultados_cifras_exactas:
        l = [r.pos_k]
        a = '≤' if r.dig_exacto else '>'
        l.append(f"E(x) {a} {r.valor_pos}")
        l.append(r.digito)
        l.append('NO es exacta' if not r.dig_exacto else 'SÍ es exacta')
        lista.append(l)

    df = pd.DataFrame(data=lista, columns=['Posición k', 'E(x) ≤ 0.5*10^k', 'Cifra o dígito', 'Exacta'])
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = 'Iteración'
    return df
