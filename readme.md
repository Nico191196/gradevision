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

## Cómo usarlo

### 1. Activar el entorno virtual

```
.\venv\Scripts\activate
```

### 2. Colocar las fotos a procesar

Poné todas las fotos de examen (formato `.jpg`, `.jpeg` o `.png`) dentro de la carpeta:

```
sample_data/exams/
```

### 3. Configurar la clave de respuestas

Editar el archivo `assets/answer_keys/clave_biologia.json` con las respuestas correctas de ese examen (una letra A/B/C/D por cada número de pregunta).

### 4. Ejecutar

```
python main.py
```

### 5. Ver los resultados

El programa genera un archivo `resultados/resultados_consolidados.csv`, que se puede abrir directamente en Excel. Incluye:
- Un resumen con la nota de cada examen procesado.
- El detalle completo de las 30 preguntas de cada uno.

## Estructura del proyecto

```
gradevision_core/
├── scanner/       → localiza y endereza la hoja en la foto
├── detection/      → encuentra las burbujas y las organiza en preguntas
├── grading/        → decide qué se marcó y compara contra la clave
└── export/         → genera el archivo de resultados
```

## Estado actual

Proyecto en desarrollo activo. Probado con fotos reales de examen; próximos pasos incluyen soporte para otros formatos de hoja y una futura versión como aplicación móvil.