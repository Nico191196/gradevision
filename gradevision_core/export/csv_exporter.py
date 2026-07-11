import csv
import os
from datetime import datetime


def exportar_resultados(resultados, correctas, total, nota, carpeta_salida="resultados", nombre_alumno="Sin especificar"):
    """
    Genera un archivo CSV con el detalle de cada pregunta y el resumen final
    de UN solo examen. (Se mantiene por si se necesita exportar de a uno).
    """
    os.makedirs(carpeta_salida, exist_ok=True)

    base_nombre = "".join(c if c.isalnum() else "_" for c in nombre_alumno)
    marca_de_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    nombre_archivo = f"resultado_{base_nombre}_{marca_de_tiempo}.csv"
    ruta_completa = os.path.join(carpeta_salida, nombre_archivo)

    with open(ruta_completa, mode="w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo, delimiter=';')

        escritor.writerow(["Alumno", nombre_alumno])
        escritor.writerow(["Correctas", "'" + f"{correctas}/{total}"])
        escritor.writerow(["Nota", "'" + f"{nota}/10"])
        escritor.writerow([])

        escritor.writerow(["Pregunta", "Marcó", "Correcta", "Resultado"])
        for r in resultados:
            estado = "Correcta" if r["es_correcta"] else "Incorrecta"
            escritor.writerow([r["pregunta"], r["marcada"], r["correcta"], estado])

    return ruta_completa


def exportar_resultados_consolidado(examenes, carpeta_salida="resultados", nombre_archivo="resultados_consolidados.csv"):
    """
    Genera un único archivo CSV con el resumen de todos los exámenes
    procesados en esta tanda, seguido del detalle pregunta por pregunta
    de cada uno.

    examenes: lista de diccionarios, cada uno con:
        {"alumno": str, "resultados": [...], "correctas": int, "total": int, "nota": float}
    """
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta_completa = os.path.join(carpeta_salida, nombre_archivo)

    with open(ruta_completa, mode="w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo, delimiter=';')

        # --- Sección 1: resumen general, una fila por examen ---
        escritor.writerow(["RESUMEN"])
        escritor.writerow(["Alumno", "Correctas", "Nota"])
        for examen in examenes:
            escritor.writerow([
                examen["alumno"],
                "'" + f"{examen['correctas']}/{examen['total']}",
                "'" + f"{examen['nota']}/10"
            ])

        escritor.writerow([])
        escritor.writerow([])

        # --- Sección 2: detalle completo de cada examen ---
        for examen in examenes:
            escritor.writerow([f"DETALLE - {examen['alumno']}"])
            escritor.writerow(["Pregunta", "Marcó", "Correcta", "Resultado"])
            for r in examen["resultados"]:
                estado = "Correcta" if r["es_correcta"] else "Incorrecta"
                escritor.writerow([r["pregunta"], r["marcada"], r["correcta"], estado])
            escritor.writerow([])

    return ruta_completa