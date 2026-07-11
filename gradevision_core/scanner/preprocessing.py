import cv2


def convertir_a_grises(imagen):
    """Convierte una imagen a color a escala de grises."""
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)


def suavizar(imagen_gris):
    """Aplica un desenfoque suave para reducir ruido/textura fina."""
    return cv2.GaussianBlur(imagen_gris, (5, 5), 0)


def detectar_bordes(imagen_suave):
    """Detecta los bordes (cambios bruscos de claro a oscuro)."""
    return cv2.Canny(imagen_suave, 75, 200)