import cv2


def cargar_imagen(ruta):
    """
    Carga una imagen desde el disco.
    Devuelve la imagen si se pudo cargar, o None si no se encontró/abrió.
    """
    return cv2.imread(ruta)