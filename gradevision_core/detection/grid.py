import cv2


def obtener_centros(burbujas):
    """
    A partir de una lista de contornos (burbujas), calcula el punto
    central (x, y) de cada uno.
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


def organizar_en_grilla(burbujas, template):
    """
    Organiza las burbujas detectadas según la configuración del template:
    'total_preguntas', 'opciones_por_pregunta', 'bloques' (columnas de
    preguntas, de izquierda a derecha).

    Devuelve una lista de 'preguntas'. Cada pregunta es una lista de
    diccionarios (uno por opción), ya ordenados de izquierda a derecha.
    """
    opciones = template["opciones_por_pregunta"]
    bloques = template["bloques"]
    preguntas_por_bloque = template["preguntas_por_bloque"]

    centros = obtener_centros(burbujas)

    esperadas = template["total_preguntas"] * opciones
    if len(centros) != esperadas:
        print(f"Aviso: se esperaban {esperadas} burbujas para armar la grilla, pero llegaron {len(centros)}.")

    # Paso 1: ordenar todo por X, y partir en 'bloques' partes iguales
    centros_por_x = sorted(centros, key=lambda c: c["cx"])
    tamano_bloque = preguntas_por_bloque * opciones

    preguntas = []
    for i in range(bloques):
        inicio = i * tamano_bloque
        fin = inicio + tamano_bloque
        bloque_actual = centros_por_x[inicio:fin]

        # Paso 2: dentro del bloque, ordenar por Y (de arriba a abajo)
        bloque_por_y = sorted(bloque_actual, key=lambda c: c["cy"])

        # Paso 3: agrupar de a 'opciones' (cada grupo = una pregunta)
        for j in range(0, len(bloque_por_y), opciones):
            fila = bloque_por_y[j:j + opciones]
            # Paso 4: dentro de la fila, ordenar por X (A, B, C, D...)
            fila_ordenada = sorted(fila, key=lambda c: c["cx"])
            preguntas.append(fila_ordenada)

    return preguntas