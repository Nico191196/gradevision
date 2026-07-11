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