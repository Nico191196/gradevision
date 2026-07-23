import cv2
import pytesseract

# Le decimos a Python exactamente dónde está instalado el programa Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def recortar_zona_nombre(hoja_enderezada, y_inicio=0.02, y_fin=0.06, x_inicio=0.10, x_fin=0.65):
    """
    Recorta la zona de la hoja donde se espera que esté escrito el
    nombre del alumno, usando porcentajes del alto/ancho de la hoja
    ya enderezada (así funciona sin importar el tamaño exacto de cada foto).
    Estos porcentajes son un punto de partida; hay que calibrarlos
    mirando el resultado real.
    """
    alto, ancho = hoja_enderezada.shape[:2]
    y1, y2 = int(alto * y_inicio), int(alto * y_fin)
    x1, x2 = int(ancho * x_inicio), int(ancho * x_fin)
    return hoja_enderezada[y1:y2, x1:x2]


def leer_nombre_ocr(recorte):
    """
    Intenta leer el texto de la zona recortada usando OCR.
    El resultado puede estar vacío o ser incorrecto (especialmente
    con letra cursiva) - por eso siempre hay que confirmarlo con
    el profesor antes de usarlo.
    """
    gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gris, lang="spa", config="--psm 7")
    return texto.strip()
