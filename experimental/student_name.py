import os
import cv2
import pytesseract
import difflib

# La ruta al ejecutable de Tesseract varia segun el sistema y la
# instalacion de cada persona (nunca hardcodear una ruta de Windows
# especifica aca). Si Tesseract no esta en el PATH del sistema, definir
# la variable de entorno TESSERACT_CMD antes de correr este script:
#
#   PowerShell:  $env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"
#   bash/zsh:    export TESSERACT_CMD="/usr/local/bin/tesseract"
_tesseract_cmd = os.environ.get("TESSERACT_CMD")
if _tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = _tesseract_cmd


def encontrar_palabra_ancla(hoja_enderezada, palabra_buscada="Alumno", similitud_minima=0.6):
    """
    Busca en toda la hoja una palabra parecida a 'palabra_buscada' usando
    OCR, y devuelve su posición (x, y, ancho, alto) si la encuentra.
    Esto permite ubicar la zona del nombre sin depender de coordenadas
    fijas, adaptándose a distintos diseños de hoja automáticamente.
    Devuelve None si no encuentra ninguna coincidencia razonable.
    """
    gris = cv2.cvtColor(hoja_enderezada, cv2.COLOR_BGR2GRAY)
    datos = pytesseract.image_to_data(gris, lang="spa", output_type=pytesseract.Output.DICT)

    mejor_coincidencia = None
    mejor_similitud = 0

    for i, palabra in enumerate(datos["text"]):
        palabra_limpia = palabra.strip().strip(":;,.").lower()
        if not palabra_limpia:
            continue

        similitud = difflib.SequenceMatcher(None, palabra_limpia, palabra_buscada.lower()).ratio()

        if similitud > mejor_similitud and similitud >= similitud_minima:
            mejor_similitud = similitud
            mejor_coincidencia = {
                "x": datos["left"][i],
                "y": datos["top"][i],
                "ancho": datos["width"][i],
                "alto": datos["height"][i]
            }

    return mejor_coincidencia


def recortar_zona_nombre_dinamico(hoja_enderezada, ancla):
    """
    Recorta la zona donde debería estar el nombre manuscrito, ubicada
    relativa a la posición real de la palabra ancla (ej: "Alumno"),
    en vez de coordenadas fijas.
    """
    alto_imagen, ancho_imagen = hoja_enderezada.shape[:2]

    x1 = ancla["x"] + ancla["ancho"]  # empieza justo después de la palabra "Alumno"
    x2 = min(x1 + ancla["ancho"] * 8, ancho_imagen)  # una franja ancha a la derecha

    # Un poco más arriba de la palabra (por si la cursiva sube), y hasta un poco más abajo
    y1 = max(0, ancla["y"] - int(ancla["alto"] * 1.2))
    y2 = ancla["y"] + int(ancla["alto"] * 1.5)

    return hoja_enderezada[y1:y2, x1:x2]


def leer_nombre_ocr(recorte):
    """
    Intenta leer el texto de la zona recortada usando OCR.
    El resultado puede ser incorrecto (especialmente con letra cursiva),
    por eso siempre hay que confirmarlo con el profesor antes de usarlo.
    """
    gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    gris_grande = cv2.resize(gris, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    binaria = cv2.adaptiveThreshold(
        gris_grande, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31, C=15
    )
    texto = pytesseract.image_to_string(binaria, lang="spa", config="--psm 7")
    return texto.strip()