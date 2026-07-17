import cv2
from gradevision_core.scanner import image_loader, preprocessing, document, perspective, student_name


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
        y_inicio=0.05, y_fin=0.10,
        x_inicio=0.05, x_fin=0.65
    )
    cv2.imwrite("recorte_nombre.png", recorte)
    print("Recorte guardado en recorte_nombre.png. Abrilo para revisar si se ve bien la zona del nombre.")

    texto = student_name.leer_nombre_ocr(recorte)
    print(f"Texto leído por OCR: '{texto}'")


if __name__ == "__main__":
    main()