import cv2
import numpy as np

ruta_imagen = "sample_data/exams/sample.jpg"
imagen = cv2.imread(ruta_imagen)

if imagen is None:
    print("No pude encontrar o abrir la imagen. Revisá el nombre y la ruta.")
else:
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    imagen_suave = cv2.GaussianBlur(imagen_gris, (5, 5), 0)
    bordes = cv2.Canny(imagen_suave, 75, 200)

    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos_ordenados = sorted(contornos, key=cv2.contourArea, reverse=True)
    contorno_hoja = contornos_ordenados[0]

    # --- NUEVO: simplificar el contorno a 4 puntos (las esquinas) ---
    perimetro = cv2.arcLength(contorno_hoja, True)
    aproximacion = cv2.approxPolyDP(contorno_hoja, 0.02 * perimetro, True)

    if len(aproximacion) != 4:
        print(f"No pude reducir el contorno a 4 esquinas exactas (encontré {len(aproximacion)}).")
        print("Puede que la foto necesite un poco más de ajuste. Por ahora, avisame para revisarlo.")
    else:
        print("¡Encontré las 4 esquinas de la hoja!")

        # --- NUEVO: ordenar las 4 esquinas de forma consistente ---
        puntos = aproximacion.reshape(4, 2)

        def ordenar_puntos(pts):
            # Ordena como: arriba-izq, arriba-der, abajo-der, abajo-izq
            suma = pts.sum(axis=1)
            diferencia = np.diff(pts, axis=1)

            ordenado = np.zeros((4, 2), dtype="float32")
            ordenado[0] = pts[np.argmin(suma)]        # arriba-izquierda (suma más chica)
            ordenado[2] = pts[np.argmax(suma)]        # abajo-derecha (suma más grande)
            ordenado[1] = pts[np.argmin(diferencia)]  # arriba-derecha
            ordenado[3] = pts[np.argmax(diferencia)]  # abajo-izquierda
            return ordenado

        esquinas = ordenar_puntos(puntos)
        (arriba_izq, arriba_der, abajo_der, abajo_izq) = esquinas

        # --- NUEVO: calcular el tamaño final de la hoja "enderezada" ---
        ancho_a = np.linalg.norm(abajo_der - abajo_izq)
        ancho_b = np.linalg.norm(arriba_der - arriba_izq)
        ancho_final = int(max(ancho_a, ancho_b))

        alto_a = np.linalg.norm(arriba_der - abajo_der)
        alto_b = np.linalg.norm(arriba_izq - abajo_izq)
        alto_final = int(max(alto_a, alto_b))

        # Los 4 puntos de destino: un rectángulo perfecto de ese tamaño
        destino = np.array([
            [0, 0],
            [ancho_final - 1, 0],
            [ancho_final - 1, alto_final - 1],
            [0, alto_final - 1]
        ], dtype="float32")

        # --- NUEVO: calcular y aplicar la transformación de perspectiva ---
        matriz = cv2.getPerspectiveTransform(esquinas, destino)
        hoja_enderezada = cv2.warpPerspective(imagen, matriz, (ancho_final, alto_final))

        def mostrar(nombre, img):
            cv2.namedWindow(nombre, cv2.WINDOW_NORMAL)
            alto, ancho = img.shape[:2]
            escala = 700 / alto
            cv2.resizeWindow(nombre, int(ancho * escala), int(alto * escala))
            cv2.imshow(nombre, img)

        mostrar("Original", imagen)
        mostrar("Hoja enderezada", hoja_enderezada)

        print("Apretá cualquier tecla para cerrar las ventanas.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()