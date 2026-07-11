import cv2
import numpy as np


def binarizar(imagen_gris):
    """
    Convierte la imagen a blanco y negro puro usando un umbral adaptativo:
    en vez de un único punto de corte para toda la hoja, calcula el mejor
    corte para cada zona pequeña por separado. Esto la hace resistente a
    sombras leves o iluminación despareja en distintas partes de la foto.
    """
    binaria = cv2.adaptiveThreshold(
        imagen_gris, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=25,  # tamaño de la zona local que analiza (debe ser impar)
        C=10           # ajuste fino de sensibilidad
    )
    return binaria


def cerrar_bordes(imagen_binaria, tam_kernel=9):
    """
    Rellena huecos pequeños (como el interior de un círculo vacío)
    para que burbujas marcadas y sin marcar den un área similar.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (tam_kernel, tam_kernel))
    return cv2.morphologyEx(imagen_binaria, cv2.MORPH_CLOSE, kernel)


def detectar_burbujas(imagen_cerrada, area_min=200, area_max=12000, tolerancia_forma=0.45):
    """
    Encuentra contornos que parezcan burbujas: tamaño razonable y forma
    aproximadamente circular (ancho similar al alto).
    """
    contornos, _ = cv2.findContours(imagen_cerrada, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    burbujas = []
    for contorno in contornos:
        (x, y, ancho, alto) = cv2.boundingRect(contorno)
        area = cv2.contourArea(contorno)
        aspecto = ancho / float(alto)

        area_ok = area_min <= area <= area_max
        forma_ok = (1 - tolerancia_forma) <= aspecto <= (1 + tolerancia_forma)

        if area_ok and forma_ok:
            burbujas.append(contorno)

    return burbujas
def diagnosticar(imagen_cerrada, area_min=200, area_max=12000, tolerancia_forma=0.45):
    """
    Similar a detectar_burbujas, pero además devuelve los contornos
    rechazados junto con sus datos, para poder entender por qué
    no pasaron el filtro.
    """
    contornos, _ = cv2.findContours(
        imagen_cerrada, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )

    aceptadas = []
    rechazadas = []

    for contorno in contornos:
        (x, y, ancho, alto) = cv2.boundingRect(contorno)
        area = cv2.contourArea(contorno)

        # Ignoramos ruido muy chico o formas gigantes (como el borde de la hoja)
        if area < 80 or area > 20000:
            continue

        aspecto = ancho / float(alto)
        area_ok = area_min <= area <= area_max
        forma_ok = (1 - tolerancia_forma) <= aspecto <= (1 + tolerancia_forma)

        if area_ok and forma_ok:
            aceptadas.append(contorno)
        else:
            rechazadas.append({"area": round(area, 1), "aspecto": round(aspecto, 2), "x": x, "y": y})

    return aceptadas, rechazadas