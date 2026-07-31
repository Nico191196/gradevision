# GradeVision — Requisitos Técnicos

## 1. Alcance de este documento

Este documento describe los requisitos técnicos del sistema GradeVision en su estado actual (pipeline de escritorio) y los requisitos técnicos necesarios para la evolución hacia un MVP con backend y frontend web móvil.

---

## 2. Estado actual del sistema

### 2.1 Componentes existentes

| Módulo | Responsabilidad |
|---|---|
| `gradevision_core/scanner` | Localización de la hoja en la foto y corrección de perspectiva |
| `gradevision_core/detection` | Detección de burbujas y organización en grilla de preguntas |
| `gradevision_core/grading` | Determinación de la respuesta marcada y calificación contra clave |
| `gradevision_core/export` | Generación de CSV consolidado, PDF individual y hoja marcada visualmente |
| `gradevision_core/templates` | Gestión de templates de examen (preguntas/opciones/bloques) y listas de alumnos (rosters) |

### 2.2 Stack tecnológico actual

- **Lenguaje**: Python 3.14
- **Visión por computadora**: OpenCV (`opencv-python`)
- **Cálculo numérico**: NumPy
- **Generación de PDF**: ReportLab
- **Testing**: pytest
- **Control de versiones**: Git, repositorio privado en GitHub
- **Entorno**: entorno virtual (`venv`), Windows

### 2.3 Requisitos funcionales cubiertos

- RF-01: El sistema debe corregir la perspectiva de una foto de examen tomada en ángulo.
- RF-02: El sistema debe detectar automáticamente las burbujas de respuesta, tolerando iluminación despareja.
- RF-03: El sistema debe determinar qué opción fue marcada por pregunta, incluyendo los casos "en blanco" y "múltiple marcada".
- RF-04: El sistema debe permitir configurar la cantidad de preguntas, opciones por pregunta, y bloques/columnas de una hoja, sin modificar código (templates).
- RF-05: El sistema debe permitir gestionar (crear, ver, editar, borrar) templates y listas de alumnos sin programar.
- RF-06: El sistema debe permitir procesar un lote de fotos, continuando el procesamiento aunque una foto individual falle.
- RF-07: El sistema debe validar la calidad de la foto (nitidez, iluminación) antes de procesar, informando errores específicos y accionables.
- RF-08: El sistema debe generar: reporte consolidado (CSV/Excel), reporte individual (PDF), e imagen de la hoja marcada visualmente (verde/rojo/amarillo por pregunta).
- RF-09: El sistema debe permitir asignar cada examen procesado a un alumno de una lista predefinida, con detección de asignaciones duplicadas dentro de una misma tanda.

### 2.4 Requisitos no funcionales cubiertos

- RNF-01 (Robustez): un fallo en el procesamiento de una foto no debe interrumpir el procesamiento del resto del lote.
- RNF-02 (Trazabilidad): todo fallo debe reportar una causa específica y una acción correctiva sugerida.
- RNF-03 (Privacidad): ningún dato identificable de alumnos (fotos, nombres, notas) debe formar parte del control de versiones del código fuente.
- RNF-04 (Mantenibilidad): la lógica de dominio (scanner/detection/grading) debe estar desacoplada de la configuración específica de cada examen (templates).
- RNF-05 (Testabilidad): la lógica de calificación y validación de configuración debe contar con tests automatizados que no dependan de fotos reales.

---

## 3. Requisitos técnicos para el MVP (Backend + Web Móvil)

### 3.1 Decisiones de arquitectura ya tomadas

- El frontend del MVP será una **aplicación web responsive** (no una app nativa), accesible desde el navegador del celular, para minimizar costo y tiempo de desarrollo.
- El backend será un servicio HTTP construido con **FastAPI** (Python), reutilizando `gradevision_core` como dependencia, sin reescribir su lógica.
- La persistencia de datos usará **SQLite** en la fase de MVP, por su costo cero y simplicidad operativa.
- El hosting del backend y frontend se hará sobre servicios con **nivel gratuito** (a evaluar entre Render, Railway o Fly.io al momento de implementar).

### 3.2 Requisitos funcionales nuevos (MVP)

- RF-10: El sistema debe exponer un endpoint HTTP para subir una foto de examen y recibir el resultado de la corrección en formato JSON.
- RF-11: El sistema debe exponer endpoints para gestionar templates, claves de respuesta y listas de alumnos vía API (equivalente web de `crear_examen.py`).
- RF-12: El sistema debe requerir autenticación de usuario (docente) para acceder a cualquier endpoint que exponga datos de exámenes, alumnos o resultados.
- RF-13: Cada docente debe poder acceder únicamente a los templates, listas de alumnos y resultados que él mismo haya creado (aislamiento por usuario).
- RF-14: El frontend debe permitir, desde el celular: iniciar sesión, seleccionar examen y lista de alumnos, subir/tomar una foto, asignar el alumno correspondiente, y visualizar el resultado con la hoja marcada.

### 3.3 Requisitos no funcionales nuevos (MVP)

- RNF-06 (Seguridad de transporte): toda comunicación entre frontend y backend debe ser HTTPS.
- RNF-07 (Seguridad de credenciales): las contraseñas de usuario deben almacenarse cifradas (hash), nunca en texto plano.
- RNF-08 (Retención de datos): las fotos originales subidas deben eliminarse automáticamente tras un período de retención configurable, conservando únicamente el resultado procesado.
- RNF-09 (Disponibilidad razonable): el backend debe funcionar de forma continua (24/7) dentro de las limitaciones del nivel gratuito del hosting elegido.
- RNF-10 (Costo): toda decisión de infraestructura debe priorizar alternativas de costo cero o mínimo, dado el carácter no lucrativo del proyecto.
- RNF-11 (Compatibilidad): el frontend debe funcionar correctamente en los navegadores móviles más comunes (Chrome/Safari en Android/iOS), sin requerir instalación.

### 3.4 Fuera de alcance del MVP (explícitamente excluido)

- Aplicación nativa (Android/iOS) instalable desde tiendas de aplicaciones.
- Servicios de OCR en la nube de pago para lectura de nombres manuscritos.
- Infraestructura de colas de procesamiento distribuido o múltiples servidores.
- Bases de datos gestionadas de pago (ej. instancias dedicadas de PostgreSQL en la nube).
- Multi-tenancy avanzado a nivel de institución (se limita a aislamiento por usuario/docente individual).

---

## 4. Requisitos de seguridad y privacidad

- Los datos de alumnos (nombre, foto, calificación) constituyen información sensible y deben tratarse conforme a principios de minimización y protección de datos aplicables (en Argentina, Ley 25.326 de Protección de Datos Personales).
- Ninguna foto ni dato identificable de alumnos debe incluirse en el repositorio de código fuente (control mediante `.gitignore`, ya implementado).
- Las contraseñas y cualquier secreto de configuración (claves de API, tokens) deben gestionarse mediante variables de entorno, nunca en el código fuente versionado.
- El acceso a resultados y datos de un docente debe estar restringido exclusivamente a su propia cuenta.

---

## 5. Requisitos de testing

- La lógica de calificación (`grading`) y validación de configuración (`templates`) debe mantener cobertura de tests automatizados (pytest).
- Antes de cada despliegue a producción, debe ejecutarse la suite completa de tests sin fallos.
- Se recomienda incorporar tests de integración para los endpoints del backend a medida que se desarrollen (Fase 1 en adelante del roadmap).
