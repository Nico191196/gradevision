import cv2
import glob
import os
import string
from gradevision_core.scanner import image_loader, preprocessing, document, perspective, validation
from gradevision_core.detection import bubbles, grid
from gradevision_core.grading import scoring, answer_key, grader
from gradevision_core.export import csv_exporter, pdf_report, visual_marker
from gradevision_core.templates import template_loader, roster_loader


def procesar_examen(ruta_imagen, clave, template):
    imagen = image_loader.cargar_imagen(ruta_imagen)
    if imagen is None:
        raise ValueError("No se pudo abrir la imagen (¿archivo dañado o formato no soportado?).")

    imagen_gris = preprocessing.convertir_a_grises(imagen)

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
        "nota": nota,
        "hoja_enderezada": hoja_enderezada,
        "preguntas": preguntas
    }


def elegir_alumno_de_lista(alumnos, ya_asignados):
    """
    Muestra la lista completa de alumnos, marcando cuáles ya fueron
    asignados en esta tanda, y devuelve el nombre elegido (por número
    de la lista, escrito directamente, o None si se deja vacío).
    """
    print("\nAlumnos:")
    for i, alumno in enumerate(alumnos, start=1):
        marca = "  (ya asignado)" if alumno in ya_asignados else ""
        print(f"  {i}. {alumno}{marca}")

    while True:
        eleccion = input(
            "\n¿A qué alumno corresponde esta hoja? "
            "(número, escribir el nombre, o Enter para usar el nombre del archivo): "
        ).strip()

        if eleccion == "":
            return None

        if eleccion.isdigit() and 1 <= int(eleccion) <= len(alumnos):
            elegido = alumnos[int(eleccion) - 1]
            if elegido in ya_asignados:
                confirmar = input(f"'{elegido}' ya fue asignado antes en esta tanda. ¿Confirmás igual? (s/n): ").strip().lower()
                if confirmar != "s":
                    continue
            return elegido

        # Si no es un número válido, lo tratamos como el nombre escrito directamente
        return eleccion


def main():
    template, clave = template_loader.elegir_examen_interactivo()

    print(f"\nUsando template: {template['nombre']}")
    print(f"({template['total_preguntas']} preguntas, {template['opciones_por_pregunta']} opciones, {template['bloques']} bloques)\n")

    rosters = roster_loader.listar_rosters()
    alumnos = []

    if rosters:
        print("=== Listas de alumnos disponibles ===")
        for i, roster in enumerate(rosters, start=1):
            print(f"  {i}. {roster['nombre']}")
        print(f"  {len(rosters) + 1}. No usar ninguna lista (nombrar los archivos manualmente)")

        while True:
            eleccion = input("\n¿Qué lista de alumnos usar? (número): ").strip()
            if eleccion.isdigit() and 1 <= int(eleccion) <= len(rosters):
                alumnos = rosters[int(eleccion) - 1]["alumnos"]
                break
            elif eleccion == str(len(rosters) + 1):
                break
            print("  Número inválido.")

    rutas_imagenes = (
        glob.glob("sample_data/exams/*.jpg")
        + glob.glob("sample_data/exams/*.jpeg")
        + glob.glob("sample_data/exams/*.png")
    )
    print(f"\nSe encontraron {len(rutas_imagenes)} fotos para procesar.\n")

    examenes_procesados = []
    ya_asignados = set()
    exitosos = 0
    fallidos = 0

    for ruta in rutas_imagenes:
        nombre_archivo = os.path.basename(ruta)
        print(f"--- Procesando: {nombre_archivo} ---")

        try:
            datos = procesar_examen(ruta, clave, template)
            print(f"Correctas: {datos['correctas']}/{datos['total']}  |  Nota: {datos['nota']}/10")

            nombre_confirmado = nombre_archivo

            if alumnos:
                elegido = elegir_alumno_de_lista(alumnos, ya_asignados)
                if elegido:
                    nombre_confirmado = elegido
                    ya_asignados.add(elegido)

            examenes_procesados.append({
                "alumno": nombre_confirmado,
                "resultados": datos["resultados"],
                "correctas": datos["correctas"],
                "total": datos["total"],
                "nota": datos["nota"]
            })
            exitosos += 1

            ruta_pdf = pdf_report.generar_pdf_examen(
                nombre_confirmado, datos["resultados"], datos["correctas"], datos["total"], datos["nota"]
            )
            print(f"PDF generado: {ruta_pdf}")

            ruta_marcada = visual_marker.marcar_hoja(
                datos["hoja_enderezada"], datos["preguntas"], datos["resultados"], nombre_archivo=nombre_confirmado
            )
            print(f"Hoja marcada generada: {ruta_marcada}")

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