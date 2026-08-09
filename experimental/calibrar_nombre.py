# Script experimental de calibracion para el OCR de nombres.
# NO forma parte del MVP (ver docs/requisitos_negocio.md) y NO se corre
# desde main.py ni desde ningun flujo activo del proyecto.
#
# ADVERTENCIA: este script llama a student_name.recortar_zona_nombre(),
# que ya no existe en student_name.py (el modulo paso a un enfoque de
# recorte dinamico por palabra ancla: recortar_zona_nombre_dinamico).
# Se conserva el script tal como estaba, sin corregir la logica, porque
# el enfoque de OCR de nombres esta descartado del MVP actual (ver
# hallazgo H9 de docs/audits/03-08-2026.md). Si en el futuro se retoma
# este camino, hay que reescribir esta llamada usando la API vigente.

import cv2
from gradevision_core.scanner import image_loader, preprocessing, document, perspective
import student_name  # modulo experimental, vive en esta misma carpeta


def main():
    ruta_imagen = "sample_data/exams/WhatsApp Image 2026-07-11 at 01.58.47.jpeg"
    imagen = image_loader.cargar_imagen(ruta_imagen)

    imagen_gris = preprocessing.convertir_a_grises(imagen)
    imagen_suave = preprocessing.suavizar(imagen_gris)
    bordes = preprocessing.detectar_bordes(imagen_suave)

    contorno_hoja = document.encontrar_contorno_hoja(bordes)
    puntos = document.obtener_cuatro_esquinas(contorno_hoja)
    esquinas = document.ordenar_esquinas(puntos)
    hoja_enderezada = perspective.enderezar_hoja(imagen, esquinas)

    recorte = student_name.recortar_zona_nombre(
        hoja_enderezada,
        y_inicio=0.082, y_fin=0.098,
        x_inicio=0.2, x_fin=0.55
    )
    cv2.imwrite("recorte_nombre.png", recorte)
    print("Recorte guardado en recorte_nombre.png. Abrilo para revisar si se ve bien la zona del nombre.")

    texto = student_name.leer_nombre_ocr(recorte)
    print(f"Texto leído por OCR: '{texto}'")


if __name__ == "__main__":
    main()