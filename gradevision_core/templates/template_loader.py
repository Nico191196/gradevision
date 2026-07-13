import json


def cargar_template(ruta):
    """
    Carga la configuración de una hoja de examen desde un archivo JSON:
    cuántas preguntas tiene en total, cuántas opciones por pregunta,
    y en cuántos bloques/columnas están distribuidas.
    """
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    total_preguntas = datos["total_preguntas"]
    opciones_por_pregunta = datos["opciones_por_pregunta"]
    bloques = datos["bloques"]

    if total_preguntas % bloques != 0:
        raise ValueError(
            f"El total de preguntas ({total_preguntas}) no se puede dividir "
            f"en partes iguales entre {bloques} bloques."
        )

    datos["preguntas_por_bloque"] = total_preguntas // bloques
    return datos

import glob
import os


def listar_examenes_disponibles(carpeta_templates="assets/templates", carpeta_claves="assets/answer_keys"):
    """
    Busca todos los templates disponibles y los empareja con su clave
    de respuestas correspondiente (mismo nombre base, generados juntos
    por crear_examen.py).
    Devuelve una lista de diccionarios: {"nombre", "ruta_template", "ruta_clave"}.
    """
    rutas_templates = glob.glob(os.path.join(carpeta_templates, "template_*.json"))

    examenes = []
    for ruta_template in rutas_templates:
        nombre_archivo = os.path.basename(ruta_template)
        base = nombre_archivo.replace("template_", "", 1)  # ej: "fisicoquimica_4to_año.json"

        ruta_clave = os.path.join(carpeta_claves, f"clave_{base}")

        if os.path.exists(ruta_clave):
            with open(ruta_template, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            examenes.append({
                "nombre": datos.get("nombre", base),
                "ruta_template": ruta_template,
                "ruta_clave": ruta_clave
            })

    return examenes


def elegir_examen_interactivo():
    """
    Muestra un menú numerado con los exámenes configurados disponibles,
    y devuelve el template y la clave ya cargados según lo que elija el profesor.
    """
    examenes = listar_examenes_disponibles()

    if not examenes:
        raise FileNotFoundError(
            "No se encontró ningún examen configurado. "
            "Ejecutá 'python crear_examen.py' primero para crear uno."
        )

    print("=== Exámenes disponibles ===")
    for i, examen in enumerate(examenes, start=1):
        print(f"  {i}. {examen['nombre']}")

    while True:
        eleccion = input("\n¿Cuál examen querés corregir? (número): ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(examenes):
            seleccionado = examenes[int(eleccion) - 1]
            break
        print("  Por favor ingresá un número válido de la lista.")

    template = cargar_template(seleccionado["ruta_template"])

    with open(seleccionado["ruta_clave"], "r", encoding="utf-8") as archivo:
        clave_datos = json.load(archivo)
    clave = {int(pregunta): letra for pregunta, letra in clave_datos.items()}

    return template, clave