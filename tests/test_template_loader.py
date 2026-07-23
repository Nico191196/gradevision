import json
import pytest
from gradevision_core.templates import template_loader


def escribir_template_temporal(tmp_path, datos):
    """
    Crea un archivo JSON temporal con los datos dados, en una carpeta
    que pytest crea y borra automáticamente para cada test (tmp_path
    es una utilidad que pytest nos da gratis para esto).
    """
    ruta = tmp_path / "template_prueba.json"
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo)
    return ruta


def test_cargar_template_valido(tmp_path):
    """Un template con números que dividen bien debe cargar sin problema."""
    ruta = escribir_template_temporal(tmp_path, {
        "nombre": "Examen de prueba",
        "total_preguntas": 30,
        "opciones_por_pregunta": 4,
        "bloques": 2
    })

    template = template_loader.cargar_template(ruta)

    assert template["preguntas_por_bloque"] == 15


def test_template_con_bloques_invalidos(tmp_path):
    """
    Si el total de preguntas no se puede dividir en partes iguales
    entre los bloques (ej: 30 preguntas en 4 bloques), debe fallar
    con un error claro, no romperse de forma confusa más adelante.
    """
    ruta = escribir_template_temporal(tmp_path, {
        "nombre": "Examen mal configurado",
        "total_preguntas": 30,
        "opciones_por_pregunta": 4,
        "bloques": 4
    })

    with pytest.raises(ValueError):
        template_loader.cargar_template(ruta)