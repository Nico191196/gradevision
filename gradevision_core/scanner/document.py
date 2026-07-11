import cv2
import numpy as np


def encontrar_contorno_hoja(bordes):
    """Busca el contorno más grande, que asumimos que es la hoja."""
    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos_ordenados = sorted(contornos, key=cv2.contourArea, reverse=True)
    return contornos_ordenados[0]


def obtener_cuatro_esquinas(contorno):
    """Simplifica un contorno a 4 esquinas. Devuelve None si no lo logra."""
    perimetro = cv2.arcLength(contorno, True)
    aproximacion = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)

    if len(aproximacion) != 4:
        print(f"  [Diagnóstico] El contorno se simplificó a {len(aproximacion)} puntos (se esperaban 4).")
        puntos_encontrados = aproximacion.reshape(-1, 2)
        print(f"  [Diagnóstico] Puntos encontrados: {puntos_encontrados.tolist()}")
        return None

    return aproximacion.reshape(4, 2)


def ordenar_esquinas(puntos):
    """Ordena 4 puntos como: arriba-izq, arriba-der, abajo-der, abajo-izq."""
    suma = puntos.sum(axis=1)
    diferencia = np.diff(puntos, axis=1)

    ordenado = np.zeros((4, 2), dtype="float32")
    ordenado[0] = puntos[np.argmin(suma)]
    ordenado[2] = puntos[np.argmax(suma)]
    ordenado[1] = puntos[np.argmin(diferencia)]
    ordenado[3] = puntos[np.argmax(diferencia)]
    return ordenado