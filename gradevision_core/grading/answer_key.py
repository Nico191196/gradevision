import json


def cargar_clave(ruta):
    """
    Carga la clave de respuestas desde un archivo JSON.
    Devuelve un diccionario como {1: "A", 2: "B", ...}
    (convertimos las claves de texto a números, para comparar más fácil).
    """
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return {int(pregunta): letra for pregunta, letra in datos.items()}