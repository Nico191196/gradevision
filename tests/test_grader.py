from gradevision_core.grading import grader


def test_calificar_todo_correcto():
    """Si el alumno marcó exactamente lo mismo que la clave, debería dar 100%."""
    clave = {1: "A", 2: "B", 3: "C"}
    respuestas = {1: "A", 2: "B", 3: "C"}

    resultados, correctas, total, nota = grader.calificar(respuestas, clave)

    assert correctas == 3
    assert total == 3
    assert nota == 10.0


def test_calificar_todo_incorrecto():
    """Si el alumno marcó todo distinto a la clave, debería dar 0."""
    clave = {1: "A", 2: "B", 3: "C"}
    respuestas = {1: "B", 2: "C", 3: "A"}

    resultados, correctas, total, nota = grader.calificar(respuestas, clave)

    assert correctas == 0
    assert nota == 0.0


def test_calificar_respuesta_en_blanco():
    """Una pregunta sin responder (None) debe contar como incorrecta, no romper nada."""
    clave = {1: "A", 2: "B"}
    respuestas = {1: "A", 2: None}

    resultados, correctas, total, nota = grader.calificar(respuestas, clave)

    assert correctas == 1
    assert nota == 5.0


def test_calificar_respuesta_multiple():
    """Una pregunta marcada como 'multiple' (dos burbujas marcadas) debe contar como incorrecta."""
    clave = {1: "A"}
    respuestas = {1: "multiple"}

    resultados, correctas, total, nota = grader.calificar(respuestas, clave)

    assert correctas == 0
    