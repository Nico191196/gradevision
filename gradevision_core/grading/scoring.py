import cv2
import numpy as np


def calcular_oscuridad_promedio(contorno, imagen_gris):
    """
    Calcula qué tan oscura es, en promedio, la zona de una burbuja
    (usando la imagen en escala de grises, sin binarizar).
    Devuelve un valor de 0 (blanco puro) a 255 (negro puro).
    """
    mascara = np.zeros(imagen_gris.shape, dtype="uint8")
    cv2.drawContours(mascara, [contorno], -1, 255, -1)

    promedio_gris = cv2.mean(imagen_gris, mask=mascara)[0]
    oscuridad = 255 - promedio_gris
    return oscuridad


def detectar_respuesta(opciones, imagen_gris, umbral_marcado=10, diferencia_minima=6):
    """
    Dada una pregunta (lista de 4 opciones A-D), calcula la oscuridad
    de cada una y la compara EN RELACIÓN a la más clara de esa misma
    fila (no contra un número fijo). Esto hace que el criterio sea
    resistente a sombras o iluminación despareja en distintas zonas
    de la hoja, porque siempre se compara contra su propio "fondo local".

    umbral_marcado: cuánto más oscura debe ser la opción marcada
                    respecto a la más clara de su misma fila.
    diferencia_minima: qué tan por delante debe estar la primera opción
                        de la segunda para no considerarlo ambiguo.
    """
    oscuridades = [
        calcular_oscuridad_promedio(opcion["contorno"], imagen_gris)
        for opcion in opciones
    ]

    base_local = min(oscuridades)  # la opción más clara de ESTA fila = referencia de "vacía"
    relativas = [o - base_local for o in oscuridades]

    mayor = max(relativas)
    indice_mayor = relativas.index(mayor)

    if mayor < umbral_marcado:
        return None, oscuridades

    otras = [r for i, r in enumerate(relativas) if i != indice_mayor]
    if otras and (mayor - max(otras)) < diferencia_minima:
        return "multiple", oscuridades

    return indice_mayor, oscuridades