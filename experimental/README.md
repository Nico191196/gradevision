# Código experimental

Esta carpeta contiene código que **no forma parte del MVP** ni de ningún
flujo activo del proyecto (`main.py`, `crear_examen.py`, el backend, etc.).
Nada de acá se instala por defecto ni se ejecuta al correr GradeVision.

## Contenido actual

### OCR de nombres (`student_name.py`, `calibrar_nombre.py`)

Prototipo evaluado para leer automáticamente el nombre del alumno desde
la hoja escaneada usando Tesseract OCR. **Se descartó explícitamente**
como parte del MVP: la lectura de letra manuscrita resultó demasiado
frágil entre distintos diseños de hoja y calidades de foto, así que el
proyecto usa selección manual del alumno desde el roster (ver
`docs/requisitos_negocio.md`).

Se conserva el código por si en el futuro se retoma esta idea con un
diseño distinto (por ejemplo, OCR con confirmación humana en vez de
como única fuente de verdad — ver Fase E del roadmap). **No se
mantiene activamente y puede estar desactualizado o directamente roto**
(`calibrar_nombre.py`, por ejemplo, llama a una función que ya no
existe en `student_name.py`).

## Cómo instalar las dependencias de esta carpeta

Este código depende de `pytesseract`, que **no** se instala con
`pip install -e ".[dev]"`. Si necesitás trabajar en esto:
pip install -e ".[ocr]"


También necesitás tener Tesseract instalado en el sistema (no viene
con `pip install pytesseract`, que solo instala el wrapper de Python).
Si el ejecutable no está en el PATH, indicá la ruta con una variable
de entorno antes de correr los scripts:
PowerShell

$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"

bash/zsh

export TESSERACT_CMD="/usr/local/bin/tesseract"

