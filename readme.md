# GradeVision

Sistema de corrección automática de exámenes de opción múltiple a partir de una foto sacada con el celular.

## ¿Qué hace?

1. Toma una foto de una hoja de examen (formato multiple choice, 30 preguntas con 4 opciones A-D).
2. Detecta automáticamente los bordes de la hoja y corrige la perspectiva (la "endereza").
3. Detecta las 120 burbujas de respuesta y determina cuál fue marcada en cada pregunta.
4. Compara las respuestas contra una clave de respuestas correctas.
5. Genera un archivo Excel (CSV) con la nota de cada examen y el detalle pregunta por pregunta.

## Reglas para sacar la foto

Para que la detección funcione correctamente:

- Dejar un margen de mesa/fondo visible en los 4 lados de la hoja (que ningún borde de la hoja llegue al límite de la foto).
- Una sola hoja de examen por foto.
- Sin dobleces ni pliegues en las esquinas de la hoja.
- Buena luz, evitando sombras fuertes sobre el papel.

## Instalación

### 1. Crear y activar el entorno virtual

python -m venv venv
.\venv\Scripts\activate


### 2. Instalar el proyecto y sus dependencias

pip install -e ".[dev]"


Esto instala `gradevision_core`, el CLI y `pytest` para correr los tests.
`pyproject.toml` es la única fuente de verdad de las dependencias del
proyecto (no hace falta tocar ningún `requirements.txt` a mano).

### 3. Verificar que todo funciona

pytest


## Cómo usarlo

### 1. Activar el entorno virtual

Si ya lo instalaste una vez, en sesiones futuras solo hace falta activarlo:

.\venv\Scripts\activate


### 2. Colocar las fotos a procesar

Poné todas las fotos de examen (formato `.jpg`, `.jpeg` o `.png`) dentro de la carpeta:

sample_data/exams/


### 3. Configurar la clave de respuestas

Editar el archivo `assets/answer_keys/clave_biologia.json` con las respuestas correctas de ese examen (una letra A/B/C/D por cada número de pregunta).

### 4. Ejecutar

python main.py


### 5. Ver los resultados

El programa genera un archivo `resultados/resultados_consolidados.csv`, que se puede abrir directamente en Excel. Incluye:
- Un resumen con la nota de cada examen procesado.
- El detalle completo de las 30 preguntas de cada uno.

## Estructura del proyecto

gradevision_core/
├── scanner/ → localiza y endereza la hoja en la foto
├── detection/ → encuentra las burbujas y las organiza en preguntas
├── grading/ → decide qué se marcó y compara contra la clave
└── export/ → genera el archivo de resultados


## Estado actual (demo de escritorio)

Lo que **hoy funciona y está probado con fotos reales**:

- Motor de visión (`gradevision_core`): detección de hoja, corrección de
  perspectiva, detección de burbujas y calificación contra una clave.
- CLI completo (`main.py`, `crear_examen.py`): procesamiento por lote,
  manejo de errores por foto, templates y rosters configurables.
- Exportación de resultados: CSV/Excel, PDF individual por alumno, y
  una imagen de la hoja con la corrección marcada visualmente.
- Asignación del alumno por selección manual desde un roster (no hay
  lectura automática de nombres manuscritos: se evaluó con OCR y se
  descartó por poco confiable — ver `experimental/README.md`).

**Este es el uso previsto hoy:** un docente con algo de comodidad en
terminal, corriendo el proceso desde su propia computadora.

## Roadmap hacia el MVP web

El objetivo final es que cualquier docente use esto **solo desde el
navegador del celular, sin instalar nada ni tocar una terminal**. Para
eso todavía falta, en orden:

1. Backend HTTP (API que exponga el motor actual, sin login) — `backend/`
   ya tiene las dependencias preparadas pero no tiene endpoints aún.
2. Persistencia con SQLite.
3. Autenticación y aislamiento de datos por usuario.
4. Política de retención de fotos.
5. Despliegue en un hosting gratuito (Render/Railway/Fly.io).
6. Cliente web móvil.

El detalle completo, con criterios de aceptación por paso, está en
`docs/roadmap.md`. El estado de cada fase y los hallazgos de la última
revisión de código están en `docs/audits/`.

> **Importante:** hasta que no esté la Fase 6 (cliente web), este
> proyecto **no** cumple todavía el objetivo de "un docente sin
> conocimientos técnicos lo usa solo desde el celular". Eso es
> intencional: se está construyendo por fases, con la demo de
> escritorio como primer hito ya alcanzado.