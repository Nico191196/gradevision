import numpy as np
import cv2
from gradevision_core.grading import scoring


def crear_imagen_con_circulos(marcado_indice):
    """
    Crea una imagen en blanco de prueba con 4 círculos en fila,
    donde uno de ellos (marcado_indice, de 0 a 3) está pintado
    de negro (simulando una burbuja marcada), y devuelve tanto
    la imagen como los 4 contornos, con la misma forma que usa
    el resto del programa: [{"contorno": ..., "cx": ..., "cy": ...}, ...]
    """
    imagen = np.full((60, 240), 255, dtype="uint8")  # imagen blanca
    opciones = []

    for i in range(4):
        centro_x = 30 + i * 60
        centro_y = 30
        radio = 15

        if i == marcado_indice:
            cv2.circle(imagen, (centro_x, centro_y), radio, 0, -1)  # relleno negro
        else:
            cv2.circle(imagen, (centro_x, centro_y), radio, 0, 2)  # solo el borde

        # Fabricamos un contorno circular aproximado para pasarle a la función
        contorno = cv2.ellipse2Poly((centro_x, centro_y), (radio, radio), 0, 0, 360, 10)
        contorno = contorno.reshape(-1, 1, 2)

        opciones.append({"contorno": contorno, "cx": centro_x, "cy": centro_y})

    return imagen, opciones


def test_detecta_la_opcion_marcada():
    """Si la opción 2 (índice 2, o sea la 'C') está rellena, debe detectarla como tal."""
    imagen, opciones = crear_imagen_con_circulos(marcado_indice=2)

    resultado, oscuridades = scoring.detectar_respuesta(opciones, imagen)

    assert resultado == 2


def test_pregunta_en_blanco():
    """Si ninguna opción está rellena (todas son solo el borde), debe devolver None."""
    imagen, opciones = crear_imagen_con_circulos(marcado_indice=-1)  # ninguna marcada

    resultado, oscuridades = scoring.detectar_respuesta(opciones, imagen)

    assert resultado is None