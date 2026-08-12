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
    Organiza las burbujas detectadas (contornos de OpenCV) según la
    configuración del template. Es un envoltorio fino sobre
    'ordenar_centros_en_grilla': calcula los centros a partir de los
    contornos y delega el resto de la lógica, que es pura (no depende
    de cv2) y por eso se puede testear con datos sintéticos.
    """
    centros = obtener_centros(burbujas)
    return ordenar_centros_en_grilla(centros, template)


def ordenar_centros_en_grilla(centros, template):
    """
    Organiza una lista de centros (diccionarios con 'cx', 'cy') según
    la configuración del template: 'total_preguntas',
    'opciones_por_pregunta', 'bloques' (columnas de preguntas, de
    izquierda a derecha), 'preguntas_por_bloque'.

    Devuelve una lista de 'preguntas'. Cada pregunta es una lista de
    diccionarios (uno por opción), ya ordenados de izquierda a derecha.

    Antes de devolver el resultado, valida que la geometría de la
    grilla sea coherente (ver 'validar_grilla_coherente'). Si algo no
    cierra -filas mezcladas, bloques superpuestos, etc.- prefiere
    fallar con un error explícito antes que devolver una grilla
    incorrecta en silencio.
    """
    opciones = template["opciones_por_pregunta"]
    bloques = template["bloques"]
    preguntas_por_bloque = template["preguntas_por_bloque"]

    esperadas = template["total_preguntas"] * opciones
    if len(centros) != esperadas:
        raise ValueError(
            f"No se puede armar la grilla: se esperaban {esperadas} burbujas "
            f"pero llegaron {len(centros)} centros calculados."
        )

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

    validar_grilla_coherente(preguntas, template)

    return preguntas


def validar_grilla_coherente(preguntas, template):
    """
    Chequea que la grilla armada por 'ordenar_centros_en_grilla' tenga
    sentido geométrico, para detectar los casos en los que el orden
    por X/Y puro mezcló burbujas de distintas filas o distintos
    bloques (columnas de preguntas). Ese tipo de error es el más
    peligroso: el pipeline no se cae, pero la nota queda mal calculada
    sin ningún aviso.

    No reemplaza al ordenamiento en sí -sigue siendo sort por X/Y-,
    sino que revisa el resultado y rechaza los casos donde la
    geometría es demasiado irregular como para confiar en él.

    Lanza ValueError con un mensaje accionable si encuentra algo
    incoherente. No devuelve nada si todo está en orden.
    """
    opciones = template["opciones_por_pregunta"]
    bloques = template["bloques"]
    preguntas_por_bloque = template["preguntas_por_bloque"]

    if not preguntas:
        return

    # --- Chequeo A: dispersión vertical dentro de cada fila ---
    # Todas las opciones de una misma pregunta deberían estar
    # prácticamente a la misma altura (misma fila). Si el rango
    # vertical de una fila es grande en relación al espaciado típico
    # entre preguntas, es señal de que se mezclaron dos filas.
    alturas_fila = []
    for pregunta in preguntas:
        cys = [c["cy"] for c in pregunta]
        alturas_fila.append(max(cys) - min(cys))

    # Espaciado típico entre preguntas consecutivas (aprox. la altura
    # de una fila), estimado a partir de los propios datos.
    centros_y_promedio = [sum(c["cy"] for c in p) / len(p) for p in preguntas]
    saltos = [
        abs(centros_y_promedio[i + 1] - centros_y_promedio[i])
        for i in range(len(centros_y_promedio) - 1)
        if centros_y_promedio[i + 1] != centros_y_promedio[i]
    ]
    salto_tipico = sorted(saltos)[len(saltos) // 2] if saltos else 0

    if salto_tipico > 0:
        limite_dispersion = salto_tipico * 0.6
        for idx, altura in enumerate(alturas_fila):
            if altura > limite_dispersion:
                raise ValueError(
                    f"Grilla incoherente en la pregunta n.º {idx + 1}: sus opciones "
                    f"no están alineadas en la misma fila (dispersión vertical de "
                    f"{altura:.0f}px, se esperaba menos de {limite_dispersion:.0f}px). "
                    f"Puede deberse a perspectiva mal corregida o rotación de la foto. "
                    f"Sacá la foto de nuevo intentando que la hoja quede lo más "
                    f"recta posible dentro del cuadro."
                )

    # --- Chequeo B: las filas de un mismo bloque deben ir de arriba
    # hacia abajo, sin retrocesos ---
    for b in range(bloques):
        preguntas_bloque = preguntas[b * preguntas_por_bloque:(b + 1) * preguntas_por_bloque]
        promedios_bloque = [sum(c["cy"] for c in p) / len(p) for p in preguntas_bloque]
        for idx in range(len(promedios_bloque) - 1):
            if promedios_bloque[idx + 1] <= promedios_bloque[idx]:
                numero_pregunta_global = b * preguntas_por_bloque + idx + 1
                raise ValueError(
                    f"Grilla incoherente cerca de la pregunta n.º {numero_pregunta_global}: "
                    f"el orden de las filas no es consistente de arriba hacia abajo. "
                    f"Puede deberse a perspectiva mal corregida o rotación de la foto. "
                    f"Sacá la foto de nuevo intentando que la hoja quede lo más "
                    f"recta posible dentro del cuadro."
                )

    # --- Chequeo C: separación entre bloques (columnas de preguntas) ---
    # Por construcción, el corte de 'ordenar_centros_en_grilla' siempre da
    # bloques sin superposición aparente (parte de una lista ya ordenada
    # por X). Eso NO garantiza que el punto de corte sea el correcto: si
    # dos bloques están muy cerca entre sí, el corte por índice puede caer
    # en cualquier lado y mezclar preguntas de una columna con la otra sin
    # que se note. Por eso, en vez de chequear superposición, se compara
    # el hueco entre bloques contra el espaciado típico entre opciones
    # dentro de una misma fila: si el hueco no es notoriamente mayor,
    # el corte no es confiable.
    if bloques > 1:
        separaciones_intra_fila = []
        for pregunta in preguntas:
            xs = sorted(c["cx"] for c in pregunta)
            for i in range(len(xs) - 1):
                separaciones_intra_fila.append(xs[i + 1] - xs[i])
        separaciones_intra_fila.sort()
        separacion_tipica = (
            separaciones_intra_fila[len(separaciones_intra_fila) // 2]
            if separaciones_intra_fila else 0
        )

        rangos_x = []
        for b in range(bloques):
            preguntas_bloque = preguntas[b * preguntas_por_bloque:(b + 1) * preguntas_por_bloque]
            xs = [c["cx"] for p in preguntas_bloque for c in p]
            rangos_x.append((min(xs), max(xs)))

        margen_minimo = separacion_tipica * 1.5
        for b in range(len(rangos_x) - 1):
            _, fin_actual = rangos_x[b]
            inicio_siguiente, _ = rangos_x[b + 1]
            hueco = inicio_siguiente - fin_actual
            if margen_minimo > 0 and hueco < margen_minimo:
                raise ValueError(
                    f"Grilla incoherente entre el bloque {b + 1} y el bloque {b + 2}: "
                    f"el hueco horizontal entre ambos ({hueco:.0f}px) es demasiado chico "
                    f"comparado con la separación típica entre opciones de una misma "
                    f"pregunta ({separacion_tipica:.0f}px). Es probable que se hayan "
                    f"mezclado preguntas de dos columnas distintas. Puede deberse a "
                    f"perspectiva mal corregida o a que los bloques del template no "
                    f"coinciden con el diseño real de la hoja."
                )