import cv2
import numpy as np


def enderezar_hoja(imagen, esquinas):
    """Estira la imagen usando las 4 esquinas para dejar la hoja de frente."""
    (arriba_izq, arriba_der, abajo_der, abajo_izq) = esquinas

    ancho_final = int(max(
        np.linalg.norm(abajo_der - abajo_izq),
        np.linalg.norm(arriba_der - arriba_izq)
    ))
    alto_final = int(max(
        np.linalg.norm(arriba_der - abajo_der),
        np.linalg.norm(arriba_izq - abajo_izq)
    ))

    destino = np.array([
        [0, 0],
        [ancho_final - 1, 0],
        [ancho_final - 1, alto_final - 1],
        [0, alto_final - 1]
    ], dtype="float32")

    matriz = cv2.getPerspectiveTransform(esquinas, destino)
    return cv2.warpPerspective(imagen, matriz, (ancho_final, alto_final))