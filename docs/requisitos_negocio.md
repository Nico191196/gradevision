# GradeVision — Requisitos de Negocio

## 1. Propósito del proyecto

GradeVision es un sistema sin fines de lucro para la corrección automática de exámenes de opción múltiple, orientado a docentes que hoy corrigen manualmente hojas de respuestas tipo bubble-sheet. El objetivo es reducir drásticamente el tiempo de corrección y minimizar errores humanos, sin requerir hardware especializado (escáneres OMR) ni conocimientos técnicos por parte del usuario final.

## 2. Problema que resuelve

- La corrección manual de exámenes de opción múltiple es lenta y propensa a errores, especialmente con cursos numerosos.
- Los escáneres OMR tradicionales son costosos y poco accesibles para instituciones educativas con recursos limitados.
- No existe una solución simple, gratuita y de bajo requerimiento técnico que permita corregir exámenes fotografiándolos con un celular común.

## 3. Usuarios objetivo

- **Usuario principal**: docentes de nivel medio/secundario (y potencialmente terciario/universitario) que toman exámenes de opción múltiple y necesitan corregirlos de forma ágil.
- **Perfil técnico esperado**: sin conocimientos de programación. La herramienta debe ser utilizable mediante interfaces simples (menús, formularios web), sin exposición a código, archivos de configuración técnica, ni terminal.
- **Contexto de uso esperado**: aulas con recursos limitados, posible conectividad inestable, uso desde dispositivos móviles personales (no equipamiento institucional dedicado).

## 4. Objetivos de negocio

- **Objetivo 1**: Ofrecer una alternativa gratuita y accesible a los sistemas de corrección OMR tradicionales.
- **Objetivo 2**: Minimizar la barrera de entrada técnica — cualquier docente debe poder usar el sistema sin asistencia técnica externa recurrente.
- **Objetivo 3**: Sostener el proyecto con costos de infraestructura nulos o mínimos, dado que no genera ingresos.
- **Objetivo 4**: Proteger la privacidad de los datos de estudiantes en todo momento, como condición no negociable del proyecto.

## 5. Alcance funcional del MVP (versión mínima viable)

### Incluido en el MVP

- Corrección automática de exámenes de opción múltiple a partir de una foto.
- Configuración de distintos formatos de examen (cantidad de preguntas, opciones, bloques) sin programar.
- Gestión de listas de alumnos por curso.
- Asignación manual (no automática) del alumno correspondiente a cada examen procesado.
- Generación de reporte consolidado (planilla) y reporte individual (PDF) por examen.
- Visualización de la hoja corregida con marcado de aciertos/errores.
- Acceso mediante navegador web desde el celular, sin necesidad de instalar una aplicación.
- Cuenta de usuario individual por docente, con aislamiento de datos entre usuarios.

### Explícitamente fuera del MVP

- Aplicación nativa descargable desde tiendas de aplicaciones.
- Lectura automática de nombres manuscritos (se resuelve mediante selección manual de una lista precargada).
- Soporte para hojas de examen con formato mixto (distinta cantidad de opciones por pregunta dentro del mismo examen).
- Gestión multi-institucional o de múltiples docentes por curso compartido.
- Integraciones con plataformas educativas externas (ej. Google Classroom).

## 6. Restricciones del proyecto

- **Restricción presupuestaria**: el proyecto no cuenta con financiamiento; toda decisión de infraestructura debe evaluarse bajo el criterio de costo cero o mínimo (niveles gratuitos de servicios de hosting/almacenamiento).
- **Restricción de mantenimiento**: al no existir un equipo dedicado, el sistema debe priorizar simplicidad operativa sobre funcionalidades avanzadas que incrementen la carga de mantenimiento.
- **Restricción legal/privacidad**: al procesar datos de menores de edad (nombre, calificación), el sistema debe cumplir con principios básicos de protección de datos personales vigentes en la jurisdicción de uso (Argentina: Ley 25.326).

## 7. Criterios de éxito del MVP

- Un docente sin conocimientos técnicos puede, sin asistencia externa: crear un examen, cargar una lista de alumnos, subir fotos desde su celular, y obtener resultados y reportes correctos.
- El sistema corrige correctamente exámenes fotografiados en condiciones reales de aula (iluminación variable, ángulos leves), con mensajes claros cuando una foto no cumple los requisitos mínimos.
- El costo operativo de mantener el sistema funcionando (hosting, almacenamiento) es cero o marginal.
- Los datos de alumnos permanecen protegidos: no expuestos en repositorios públicos, con acceso restringido por usuario, y con políticas de retención de fotos definidas.

## 8. Stakeholders

- **Responsable del proyecto / desarrollador principal**: Nicolás (docente, propietario del proyecto).
- **Usuarios finales**: docentes que adopten la herramienta.
- **Beneficiarios indirectos**: instituciones educativas y estudiantes, mediante la reducción de tiempos de corrección y errores.

## 9. Supuestos

- Los docentes usuarios cuentan con acceso a un teléfono celular con cámara y conexión a internet, al menos intermitente.
- Las hojas de examen siguen un formato de bubble-sheet estándar (opción múltiple, círculos a rellenar), configurable pero no arbitrariamente libre.
- El volumen de uso esperado en el MVP es acorde a uso individual o de pocos docentes simultáneos, compatible con los límites de los niveles gratuitos de hosting.
