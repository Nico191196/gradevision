# gradevision_core

Motor de visión por computadora y calificación de exámenes de opción múltiple, usado por el proyecto GradeVision. Este paquete es agnóstico de interfaz (no sabe nada de terminal, web, ni base de datos) — solo procesa imágenes y calcula resultados.

## Instalación (desde otro proyecto)

Con el entorno virtual del proyecto que lo va a usar activado, parado en la raíz de GradeVision (donde está `pyproject.toml`): 

pip install -e /ruta/a/Gradevision

O, si el proyecto que lo consume vive en una subcarpeta del mismo repositorio (como será el caso de `backend/`):

pip install -e ../..

## Uso básico

```python
from gradevision_core.scanner import image_loader, preprocessing, document, perspective
from gradevision_core.detection import bubbles, grid
from gradevision_core.grading import scoring, grader
from gradevision_core.templates import template_loader

# 1. Cargar y enderezar la imagen
imagen = image_loader.cargar_imagen("ruta/a/la/foto.jpg")
imagen_gris = preprocessing.convertir_a_grises(imagen)
imagen_suave = preprocessing.suavizar(imagen_gris)
bordes = preprocessing.detectar_bordes(imagen_suave)

contorno_hoja = document.encontrar_contorno_hoja(bordes)
puntos = document.obtener_cuatro_esquinas(contorno_hoja)
esquinas = document.ordenar_esquinas(puntos)
hoja_enderezada = perspective.enderezar_hoja(imagen, esquinas)

# 2. Detectar burbujas y organizarlas según un template
template = template_loader.cargar_template("ruta/al/template.json")
# ...detectar burbujas, organizar en grilla, calificar...
```

Para el flujo completo de principio a fin, ver `main.py` en la raíz del repositorio — es el ejemplo de referencia de cómo se conectan todos los módulos.

## Estructura de módulos

| Módulo | Responsabilidad |
|---|---|
| `scanner` | Localización de la hoja y corrección de perspectiva |
| `detection` | Detección de burbujas y organización en grilla |
| `grading` | Determinación de respuestas y calificación |
| `export` | Generación de CSV, PDF y hoja marcada visualmente |
| `templates` | Gestión de configuración de exámenes y listas de alumnos |

## Notas para quien lo consuma desde un backend

- Todas las funciones reciben las rutas de archivo como parámetros (o con valores por defecto sobreescribibles) — no asumen ninguna estructura de carpetas fija.
- Ninguna función imprime a consola ni pide `input()` salvo las de `templates/template_editor.py` y `templates/roster_loader.py`, que son específicamente para uso interactivo por terminal (no deberían usarse desde un backend; en su lugar, crear/editar templates y rosters directamente contra la base de datos).