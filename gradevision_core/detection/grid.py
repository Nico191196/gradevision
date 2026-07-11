import cv2


def obtener_centros(burbujas):
    """
    A partir de una lista de contornos (burbujas), calcula el punto
    central (x, y) de cada uno. Devuelve una lista de diccionarios
    con el contorno original y su centro.
    """
    centros = []
    for contorno in burbujas:
        momentos = cv2.moments(contorno)
        if momentos["m00"] == 0:
            continue
        cx = int(momentos["m10"] / momentos["m00"])
        cy = int(momentos["m01"] / momentos["m00"])
        centros.append({"contorno": contorno, "cx": cx, "cy": cy})
    return centros


def organizar_en_grilla(burbujas, preguntas_por_bloque=15, opciones=4):
    """
    Organiza las burbujas detectadas en la estructura lógica de la hoja:
    2 bloques de preguntas (izquierda y derecha), cada uno con filas
    (preguntas) y columnas (opciones A, B, C, D).

    Devuelve una lista de 'preguntas'. Cada pregunta es una lista de 4
    diccionarios (uno por opción), ya ordenados A, B, C, D.
    """
    centros = obtener_centros(burbujas)

    esperadas = preguntas_por_bloque * opciones * 2
    if len(centros) != esperadas:
        print(f"Aviso: se esperaban {esperadas} burbujas para armar la grilla, pero llegaron {len(centros)}.")

    # Paso 1: separar en bloque izquierdo y derecho según la posición X
    centros_por_x = sorted(centros, key=lambda c: c["cx"])
    mitad = len(centros_por_x) // 2
    bloque_izquierdo = centros_por_x[:mitad]
    bloque_derecho = centros_por_x[mitad:]

    preguntas = []
    for bloque in (bloque_izquierdo, bloque_derecho):
        # Paso 2: dentro del bloque, ordenar por Y (de arriba a abajo)
        bloque_por_y = sorted(bloque, key=lambda c: c["cy"])

        # Paso 3: agrupar de a 4 (cada grupo de 4 = una pregunta)
        for i in range(0, len(bloque_por_y), opciones):
            fila = bloque_por_y[i:i + opciones]
            # Paso 4: dentro de la fila, ordenar por X para tener A, B, C, D
            fila_ordenada = sorted(fila, key=lambda c: c["cx"])
            preguntas.append(fila_ordenada)

    return preguntas