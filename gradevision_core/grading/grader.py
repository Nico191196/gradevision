def calificar(respuestas_detectadas, clave):
    """
    Compara las respuestas detectadas contra la clave.
    respuestas_detectadas: diccionario {numero_pregunta: "A"/"B"/"C"/"D"/None/"multiple"}
    clave: diccionario {numero_pregunta: "A"/"B"/"C"/"D"}

    Devuelve una lista de resultados por pregunta y el puntaje total.
    """
    resultados = []
    correctas = 0

    for num_pregunta in sorted(clave.keys()):
        respuesta_correcta = clave[num_pregunta]
        respuesta_marcada = respuestas_detectadas.get(num_pregunta)

        es_correcta = respuesta_marcada == respuesta_correcta
        if es_correcta:
            correctas += 1

        resultados.append({
            "pregunta": num_pregunta,
            "marcada": respuesta_marcada,
            "correcta": respuesta_correcta,
            "es_correcta": es_correcta
        })

    total_preguntas = len(clave)
    nota_sobre_10 = round((correctas / total_preguntas) * 10, 2)

    return resultados, correctas, total_preguntas, nota_sobre_10