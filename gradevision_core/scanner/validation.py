import cv2
import numpy as np


def verificar_nitidez(imagen_gris, umbral_minimo=80):
    """
    Mide qué tan nítida es la imagen usando la varianza del Laplaciano
    (una técnica estándar): una foto borrosa tiene transiciones de
    color más "suaves", lo que da una varianza baja. Una foto nítida
    tiene bordes marcados, con varianza alta.
    Devuelve (es_nitida: bool, valor_medido: float).
    """
    varianza = cv2.Laplacian(imagen_gris, cv2.CV_64F).var()
    return varianza >= umbral_minimo, varianza


def verificar_iluminacion(imagen_gris, minimo=40, maximo=220):
    """
    Verifica que el brillo promedio de la imagen esté en un rango
    razonable (ni demasiado oscura, ni sobreexpuesta/quemada).
    Devuelve (es_valida: bool, valor_medido: float).
    """
    brillo_promedio = float(np.mean(imagen_gris))
    return minimo <= brillo_promedio <= maximo, brillo_promedio


def diagnosticar_falla_esquinas(puntos, ancho_imagen, alto_imagen, margen_borde=5):
    """
    Da un mensaje específico sobre por qué no se pudo detectar un
    rectángulo limpio de 4 esquinas, basándose en patrones ya
    identificados en pruebas reales:
    - Si algún punto está pegado al borde de la imagen: falta margen.
    - Si el contorno es muy chico respecto a la imagen: no encontró
      la hoja en absoluto (probablemente agarró otra cosa).
    - En cualquier otro caso: probable pliegue en la hoja o más de
      una hoja visible en la foto.
    """
    puntos = np.array(puntos)
    x_min, y_min = puntos.min(axis=0)
    x_max, y_max = puntos.max(axis=0)

    ancho_contorno = x_max - x_min
    alto_contorno = y_max - y_min
    area_contorno = ancho_contorno * alto_contorno
    area_imagen = ancho_imagen * alto_imagen

    toca_borde = (
        x_min <= margen_borde or y_min <= margen_borde or
        x_max >= ancho_imagen - margen_borde or y_max >= alto_imagen - margen_borde
    )

    # Si el contorno es chico comparado con la foto, no encontró la hoja real
    if area_contorno < area_imagen * 0.2:
        return (
            "No se detectó la hoja (el contorno encontrado es muy chico). "
            "Probablemente falte contraste entre la hoja y el fondo, o haya "
            "poca luz. Sacá la foto de nuevo con buena luz y un fondo que "
            "contraste con el papel."
        )

    if toca_borde:
        return (
            "El borde de la hoja llega hasta el límite de la foto. "
            "Sacá la foto de nuevo dejando un margen de mesa/fondo visible "
            "en los 4 lados de la hoja."
        )

    return (
        "El contorno de la hoja no forma un rectángulo limpio de 4 esquinas. "
        "Revisá que la hoja no tenga pliegues ni esquinas dobladas, y que "
        "en la foto se vea una sola hoja (sin otra hoja o papel superpuesto)."
    )