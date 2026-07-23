import cv2
import os
import numpy as np

def marcar_hoja(hoja_enderezada, preguntas, resultados, carpeta_salida="resultados/marcadas", nombre_archivo="examen"):
    """
    Dibuja sobre una copia de la hoja enderezada las marcas de corrección:
    - Círculo verde alrededor de la opción marcada, si es correcta.
    - Círculo rojo alrededor de la opción marcada, si es incorrecta,
      junto con una marca amarilla en la opción que era la correcta.

    preguntas: la lista que devuelve grid.organizar_en_grilla (con
               el contorno y centro de cada opción, en orden).
    resultados: la lista que devuelve grader.calificar (con el detalle
                de cada pregunta: marcada, correcta, es_correcta).

    Devuelve la ruta del archivo generado.
    """
    hoja_marcada = hoja_enderezada.copy()
    letras = "ABCDEFGHIJ"  # alcanza hasta 10 opciones, más que suficiente

    for r in resultados:
        num_pregunta = r["pregunta"]
        opciones_pregunta = preguntas[num_pregunta - 1]  # -1 porque la lista empieza en 0

        radio = int(np.ptp(opciones_pregunta[0]["contorno"][:, :, 0]) / 1.6)

        if r["es_correcta"]:
            # Marcar en verde la opción marcada (que además es la correcta)
            indice_marcada = letras.index(r["marcada"])
            centro = (opciones_pregunta[indice_marcada]["cx"], opciones_pregunta[indice_marcada]["cy"])
            cv2.circle(hoja_marcada, centro, radio, (0, 200, 0), 3)

        else:
            # Marcar en rojo lo que el alumno marcó (si marcó algo reconocible)
            if r["marcada"] is not None and r["marcada"] in letras:
                indice_marcada = letras.index(r["marcada"])
                centro_marcada = (opciones_pregunta[indice_marcada]["cx"], opciones_pregunta[indice_marcada]["cy"])
                cv2.circle(hoja_marcada, centro_marcada, radio, (0, 0, 220), 3)

            # Marcar en amarillo cuál era la opción correcta
            indice_correcta = letras.index(r["correcta"])
            centro_correcta = (opciones_pregunta[indice_correcta]["cx"], opciones_pregunta[indice_correcta]["cy"])
            cv2.circle(hoja_marcada, centro_correcta, radio, (0, 220, 220), 3)

    os.makedirs(carpeta_salida, exist_ok=True)
    base_nombre = "".join(c if c.isalnum() else "_" for c in nombre_archivo)
    ruta = os.path.join(carpeta_salida, f"{base_nombre}_marcada.png")
    cv2.imwrite(ruta, hoja_marcada)

    return ruta