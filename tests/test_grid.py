import math
import random
import pytest
from gradevision_core.detection import grid


# --- Helpers para generar grillas sintéticas ---
#
# En vez de fabricar imágenes y contornos falsos, se trabaja directo
# sobre 'centros' (diccionarios con cx/cy), que es lo que
# 'ordenar_centros_en_grilla' recibe una vez que ya se calcularon los
# centros de cada burbuja. Esto permite escribir escenarios de
# geometría controlada (grillas perfectas, rotadas, con huecos chicos
# entre bloques, etc.) sin depender de OpenCV ni de fotos reales.


def generar_centros_perfectos(template, ancho_opcion=60, alto_fila=80,
                               x_inicio=100, sep_entre_bloques=200, y_inicio=100):
    """
    Genera centros sintéticos organizados exactamente según la
    geometría esperada del template: cada bloque es una columna de
    preguntas, cada pregunta una fila de 'opciones' burbujas
    espaciadas uniformemente.

    A cada centro se le agrega un 'id' = (bloque, pregunta, opcion)
    para poder verificar después si 'ordenar_centros_en_grilla' los
    agrupó y ordenó correctamente.

    Devuelve (centros, orden_esperado), donde orden_esperado es una
    lista de preguntas (cada una, una lista de centros en el orden
    correcto A, B, C...).
    """
    opciones = template["opciones_por_pregunta"]
    bloques = template["bloques"]
    preguntas_por_bloque = template["preguntas_por_bloque"]

    centros = []
    orden_esperado = []

    x_bloque = x_inicio
    for b in range(bloques):
        y = y_inicio
        for p in range(preguntas_por_bloque):
            fila = []
            for o in range(opciones):
                centro = {"cx": x_bloque + o * ancho_opcion, "cy": y, "id": (b, p, o)}
                centros.append(centro)
                fila.append(centro)
            orden_esperado.append(fila)
            y += alto_fila
        x_bloque += (opciones - 1) * ancho_opcion + sep_entre_bloques

    return centros, orden_esperado


def rotar_centros(centros, angulo_grados, origen):
    """
    Rota una lista de centros alrededor de un punto 'origen', para
    simular una hoja con rotación o perspectiva residual (foto no
    perfectamente enderezada).
    """
    angulo = math.radians(angulo_grados)
    ox, oy = origen
    rotados = []
    for c in centros:
        dx, dy = c["cx"] - ox, c["cy"] - oy
        nuevo_cx = ox + dx * math.cos(angulo) - dy * math.sin(angulo)
        nuevo_cy = oy + dx * math.sin(angulo) + dy * math.cos(angulo)
        rotados.append({**c, "cx": nuevo_cx, "cy": nuevo_cy})
    return rotados


def ids_en_orden(preguntas):
    """Extrae solo los 'id' de cada pregunta, para comparar contra el orden esperado."""
    return [[c["id"] for c in pregunta] for pregunta in preguntas]


TEMPLATE_DOS_BLOQUES = {
    "total_preguntas": 30,
    "opciones_por_pregunta": 4,
    "bloques": 2,
    "preguntas_por_bloque": 15,
}

TEMPLATE_UN_BLOQUE = {
    "total_preguntas": 20,
    "opciones_por_pregunta": 3,
    "bloques": 1,
    "preguntas_por_bloque": 20,
}


# --- Casos sanos: la grilla debe ordenarse correctamente ---

def test_grilla_perfecta_dos_bloques_se_ordena_correctamente():
    """
    Con una grilla perfecta (sin ruido) y el orden de entrada mezclado
    (como llegaría de la detección real de contornos), el resultado
    debe coincidir exactamente con el orden lógico esperado.
    """
    centros, orden_esperado = generar_centros_perfectos(TEMPLATE_DOS_BLOQUES)
    random.Random(42).shuffle(centros)

    resultado = grid.ordenar_centros_en_grilla(centros, TEMPLATE_DOS_BLOQUES)

    assert ids_en_orden(resultado) == ids_en_orden(orden_esperado)


def test_grilla_perfecta_un_bloque_se_ordena_correctamente():
    """Mismo chequeo que el anterior, pero con un template de un solo bloque."""
    centros, orden_esperado = generar_centros_perfectos(
        TEMPLATE_UN_BLOQUE, ancho_opcion=50, alto_fila=45
    )
    random.Random(7).shuffle(centros)

    resultado = grid.ordenar_centros_en_grilla(centros, TEMPLATE_UN_BLOQUE)

    assert ids_en_orden(resultado) == ids_en_orden(orden_esperado)


def test_grilla_con_jitter_leve_sigue_siendo_correcta():
    """
    Un poco de ruido en las coordenadas (como el que produce una foto
    real, muy por debajo del espaciado entre burbujas) no debería
    afectar el resultado ni disparar la validación.
    """
    centros, orden_esperado = generar_centros_perfectos(TEMPLATE_DOS_BLOQUES)
    aleatorio = random.Random(7)
    con_jitter = [
        {**c, "cx": c["cx"] + aleatorio.uniform(-4, 4), "cy": c["cy"] + aleatorio.uniform(-4, 4)}
        for c in centros
    ]
    aleatorio.shuffle(con_jitter)

    resultado = grid.ordenar_centros_en_grilla(con_jitter, TEMPLATE_DOS_BLOQUES)

    assert ids_en_orden(resultado) == ids_en_orden(orden_esperado)


# --- Casos de geometría incoherente: debe rechazar, nunca calificar mal en silencio ---

def test_grilla_rotada_se_rechaza_en_vez_de_calificar_mal():
    """
    Este es el caso central de H6 (auditoría 03-08-2026): con suficiente
    rotación residual, el ordenamiento por X/Y puro puede mezclar filas
    sin ningún error visible, produciendo una nota incorrecta. La
    validación geométrica tiene que detectar esta situación y frenar
    el proceso con un error explícito, en vez de devolver una grilla
    mal armada.
    """
    centros, _ = generar_centros_perfectos(TEMPLATE_DOS_BLOQUES)
    rotados = rotar_centros(centros, angulo_grados=18, origen=(400, 700))

    with pytest.raises(ValueError, match="Grilla incoherente"):
        grid.ordenar_centros_en_grilla(rotados, TEMPLATE_DOS_BLOQUES)


def test_bloques_muy_juntos_se_rechazan():
    """
    Si dos bloques (columnas de preguntas) quedan demasiado cerca entre
    sí -o incluso invertidos en el eje X-, el corte por índice puede
    mezclar preguntas de una columna con la otra sin que el ordenamiento
    por sí solo lo note (ver Chequeo C en validar_grilla_coherente).
    """
    centros, _ = generar_centros_perfectos(TEMPLATE_DOS_BLOQUES, sep_entre_bloques=-250)

    with pytest.raises(ValueError, match="Grilla incoherente"):
        grid.ordenar_centros_en_grilla(centros, TEMPLATE_DOS_BLOQUES)


def test_opcion_desplazada_a_otra_fila_se_rechaza():
    """
    Si una sola burbuja quedó mal detectada y su centro cae a mitad de
    camino entre dos filas (por ejemplo, por una mancha o un contorno
    mal calculado), la dispersión vertical de esa pregunta debe delatar
    el problema (Chequeo A), aunque el resto de la hoja esté perfecta.
    """
    centros, _ = generar_centros_perfectos(TEMPLATE_UN_BLOQUE, ancho_opcion=50, alto_fila=45)
    # Empujamos una sola burbuja (la primera) bien lejos de su fila real,
    # a más de la mitad del espaciado entre filas (45px).
    centros[0] = {**centros[0], "cy": centros[0]["cy"] + 35}

    with pytest.raises(ValueError, match="Grilla incoherente"):
        grid.ordenar_centros_en_grilla(centros, TEMPLATE_UN_BLOQUE)


def test_cantidad_de_centros_distinta_a_la_esperada_lanza_error():
    """
    Si por algún motivo llega una cantidad de centros distinta a la
    esperada por el template, debe frenar con un error claro en vez de
    intentar armar una grilla con las cuentas mal.
    """
    centros, _ = generar_centros_perfectos(TEMPLATE_UN_BLOQUE, ancho_opcion=50, alto_fila=45)
    centros_incompletos = centros[:-1]

    with pytest.raises(ValueError, match="se esperaban"):
        grid.ordenar_centros_en_grilla(centros_incompletos, TEMPLATE_UN_BLOQUE)