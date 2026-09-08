"""
Analizador y Generador Musical.

El programa analiza y genera progresiones de acordes

"""

#Bibliotecas
import random

#constante
NOTAS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]


"""
================== funciones musicales =========================
"""



def generar_escala_mayor(nota):
   
    """
    La escala mayor esta compuesta de T, T, S, T, T, T, S. (Tono/Semitono)
    1 tono son 2 semitonos, es por esto que hacemos los intervalos
    matemáticamente de esta forma:

    """
    intervalos = [2, 2, 1, 2, 2, 2, 1]
    #Buscamos la posición de la nota (0-11) que establecimos arriba
    indice_nota = NOTAS.index(nota)
    #Será la escala de la nota que recibimos
    escala = [nota]

    #Para todos los intervalos del (intervalo) menos el último
    for intervalo in intervalos[:-1]:
        #La siguiente nota de la escala mayor será determinada por:
        indice_nota = (indice_nota + intervalo) % len(NOTAS)
        #Agregamos las notas que salgan al final de una lista
        escala.append(NOTAS[indice_nota])

    return escala


def tests():
    """
    Hace pruebas de las funciones musicales.
    """

    resultado = generar_escala_mayor("B")

    esperado = ["B", "C#", "D#", "E", "F#", "G#", "A#"]

    assert resultado == esperado

    print("Todas las pruebas fueron exitosas.")



tests()
