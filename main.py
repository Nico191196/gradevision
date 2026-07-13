import cv2
import glob
import os
import string
from gradevision_core.scanner import image_loader, preprocessing, document, perspective, validation
from gradevision_core.detection import bubbles, grid
from gradevision_core.grading import scoring, answer_key, grader
from gradevision_core.export import csv_exporter
from gradevision_core.templates import template_loader


def procesar_examen(ruta_imagen, clave, template):
    imagen = image_loader.cargar_imagen(ruta_imagen)
    if imagen is None:
        raise ValueError("No se pudo abrir la imagen (¿archivo dañado o formato no soportado?).")

    imagen_gris = preprocessing.convertir_a_grises(imagen)

    # --- Validaciones tempranas de calidad de la foto ---
    nitida, valor_nitidez = validation.verificar_nitidez(imagen_gris)
    if not nitida:
        raise ValueError(
            f"La foto parece estar borrosa (nitidez medida: {valor_nitidez:.1f}, "
            f"mínimo esperado: 80). Sacá la foto de nuevo con la cámara estable y bien enfocada."
        )

    iluminacion_ok, valor_brillo = validation.verificar_iluminacion(imagen_gris)
    if not iluminacion_ok:
        raise ValueError(
            f"La iluminación de la foto no es adecuada (brillo medido: {valor_brillo:.1f}). "
            f"Sacá la foto de nuevo con mejor luz, evitando sombras fuertes o luz directa excesiva."
        )

    imagen_suave = preprocessing.suavizar(imagen_gris)
    bordes = preprocessing.detectar_bordes(imagen_suave)

    contorno_hoja = document.encontrar_contorno_hoja(bordes)
    puntos = document.obtener_cuatro_esquinas(contorno_hoja)

    if puntos is None:
        # Diagnóstico inteligente: para esto necesitamos los puntos "crudos"
        # (sin simplificar a 4), así que los recalculamos acá para el mensaje.
        perimetro = cv2.arcLength(contorno_hoja, True)
        aproximacion = cv2.approxPolyDP(contorno_hoja, 0.02 * perimetro, True)
        puntos_crudos = aproximacion.reshape(-1, 2)

        alto_imagen, ancho_imagen = imagen.shape[:2]
        mensaje = validation.diagnosticar_falla_esquinas(puntos_crudos, ancho_imagen, alto_imagen)
        raise ValueError(mensaje)

    esquinas = document.ordenar_esquinas(puntos)
    hoja_enderezada = perspective.enderezar_hoja(imagen, esquinas)

    hoja_gris = preprocessing.convertir_a_grises(hoja_enderezada)
    hoja_binaria = bubbles.binarizar(hoja_gris)
    hoja_cerrada = bubbles.cerrar_bordes(hoja_binaria)
    burbujas_encontradas = bubbles.detectar_burbujas(hoja_cerrada)

    total_esperado = template["total_preguntas"] * template["opciones_por_pregunta"]
    if len(burbujas_encontradas) != total_esperado:
        raise ValueError(
            f"Se esperaban {total_esperado} burbujas, se detectaron {len(burbujas_encontradas)}. "
            f"Revisá que no haya marcas ajenas a las respuestas (tildes, cruces, manchas) cerca de las burbujas."
        )

    preguntas = grid.organizar_en_grilla(burbujas_encontradas, template)

    letras = list(string.ascii_uppercase[:template["opciones_por_pregunta"]])
    respuestas_detectadas = {}

    for num_pregunta, opciones in enumerate(preguntas, start=1):
        resultado, _ = scoring.detectar_respuesta(opciones, hoja_gris)
        if resultado is None:
            respuestas_detectadas[num_pregunta] = None
        elif resultado == "multiple":
            respuestas_detectadas[num_pregunta] = "multiple"
        else:
            respuestas_detectadas[num_pregunta] = letras[resultado]

    resultados, correctas, total, nota = grader.calificar(respuestas_detectadas, clave)

    return {
        "resultados": resultados,
        "correctas": correctas,
        "total": total,
        "nota": nota
    }


def main():
    template, clave = template_loader.elegir_examen_interactivo()
    
    print(f"Usando template: {template['nombre']}")
    print(f"({template['total_preguntas']} preguntas, {template['opciones_por_pregunta']} opciones, {template['bloques']} bloques)\n")

    rutas_imagenes = (
        glob.glob("sample_data/exams/*.jpg")
        + glob.glob("sample_data/exams/*.jpeg")
        + glob.glob("sample_data/exams/*.png")
    )
    print(f"Se encontraron {len(rutas_imagenes)} fotos para procesar.\n")

    examenes_procesados = []
    exitosos = 0
    fallidos = 0

    for ruta in rutas_imagenes:
        nombre_archivo = os.path.basename(ruta)
        print(f"--- Procesando: {nombre_archivo} ---")

        try:
            datos = procesar_examen(ruta, clave, template)
            print(f"Correctas: {datos['correctas']}/{datos['total']}  |  Nota: {datos['nota']}/10")

            examenes_procesados.append({
                "alumno": nombre_archivo,
                "resultados": datos["resultados"],
                "correctas": datos["correctas"],
                "total": datos["total"],
                "nota": datos["nota"]
            })
            exitosos += 1

        except ValueError as error:
            print(f"FALLÓ: {error}")
            fallidos += 1

        print()

    if examenes_procesados:
        ruta_csv = csv_exporter.exportar_resultados_consolidado(examenes_procesados)
        print(f"Archivo consolidado generado en: {ruta_csv}")

    print(f"\n--- Resumen final: {exitosos} procesados con éxito, {fallidos} fallidos ---")


if __name__ == "__main__":
    main()