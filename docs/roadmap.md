# GradeVision — Roadmap Secuencial del MVP

Este roadmap desglosa cada fase del plan de MVP en pasos secuenciales, cada uno con un criterio de aceptación verificable, para poder avanzar de a uno sin perder de vista el orden de dependencias.

---

## Fase 0 — Preparar `gradevision_core` como librería reutilizable

1. **Paso 0.1**: Crear `gradevision_core/pyproject.toml`, declarando el paquete como instalable.
   - *Criterio de aceptación*: `pip install -e .` desde la raíz del proyecto instala `gradevision_core` sin errores.
2. **Paso 0.2**: Revisar que ningún módulo de `gradevision_core` dependa de rutas absolutas o de la estructura de carpetas de `main.py`.
   - *Criterio de aceptación*: los tests actuales (`pytest`) siguen pasando tras la revisión.
3. **Paso 0.3**: Documentar en `gradevision_core/README.md` cómo importar y usar el paquete desde otro proyecto (el futuro backend).
   - *Criterio de aceptación*: siguiendo únicamente ese README, es posible importar `gradevision_core` desde un script nuevo, fuera de la carpeta actual del proyecto.

---

## Fase 1 — Backend mínimo local (sin base de datos ni login)

4. **Paso 1.1**: Instalar FastAPI y Uvicorn en un entorno virtual nuevo, separado del proyecto actual (`backend/venv`).
   - *Criterio de aceptación*: `uvicorn main:app --reload` levanta un servidor local sin errores.
5. **Paso 1.2**: Crear `backend/app/main.py` con un endpoint `GET /health` que responda `{"status": "ok"}`.
   - *Criterio de aceptación*: acceder a `http://localhost:8000/health` desde el navegador devuelve la respuesta esperada.
6. **Paso 1.3**: Crear el endpoint `POST /procesar`, que reciba una imagen y parámetros de template/clave (aún hardcodeados o pasados a mano), y devuelva el resultado de `gradevision_core` en JSON.
   - *Criterio de aceptación*: subiendo una foto de prueba desde `/docs` (la interfaz automática de FastAPI), se recibe el mismo resultado (correctas, nota, detalle) que produce `main.py` hoy con esa misma foto.
7. **Paso 1.4**: Manejar errores del pipeline (ej. foto borrosa, esquinas no detectadas) devolviendo un código de error HTTP apropiado y el mensaje descriptivo ya existente.
   - *Criterio de aceptación*: subir una foto defectuosa de prueba devuelve un error claro en el JSON de respuesta, sin que el servidor se caiga.

---

## Fase 2 — Persistencia con SQLite

8. **Paso 2.1**: Diseñar el esquema de base de datos: tablas `usuarios`, `templates`, `claves_respuesta`, `rosters`, `alumnos`, `resultados`.
   - *Criterio de aceptación*: el esquema está documentado (diagrama o listado de tablas/columnas) antes de escribir código.
9. **Paso 2.2**: Implementar el acceso a datos (usando SQLAlchemy u otra librería equivalente) y crear la base de datos vacía localmente.
   - *Criterio de aceptación*: se puede insertar y leer un registro de prueba en cada tabla desde un script simple.
10. **Paso 2.3**: Migrar los datos existentes (`assets/templates/*.json`, `assets/answer_keys/*.json`, `assets/rosters/*.json`) a la base de datos mediante un script de migración único.
    - *Criterio de aceptación*: tras la migración, los templates y listas de alumnos ya creados aparecen correctamente en la base de datos.
11. **Paso 2.4**: Adaptar los endpoints existentes para leer/escribir desde la base de datos en vez de archivos JSON sueltos.
    - *Criterio de aceptación*: `POST /procesar` sigue funcionando igual que en la Fase 1, ahora obteniendo el template/clave desde la base de datos.

---

## Fase 3 — Autenticación de usuarios

12. **Paso 3.1**: Crear el endpoint `POST /registro` (alta de usuario docente) y `POST /login` (devuelve un token de sesión JWT).
    - *Criterio de aceptación*: registrar un usuario de prueba y loguearse devuelve un token válido.
13. **Paso 3.2**: Proteger todos los endpoints de datos (templates, rosters, resultados) para que requieran un token válido.
    - *Criterio de aceptación*: acceder a un endpoint protegido sin token devuelve error 401 (no autorizado).
14. **Paso 3.3**: Asociar cada template, roster y resultado al usuario que lo creó, y filtrar las consultas para que cada usuario solo vea lo propio.
    - *Criterio de aceptación*: con dos usuarios de prueba, cada uno ve únicamente sus propios templates y resultados, nunca los del otro.

---

## Fase 4 — Manejo seguro de fotos

15. **Paso 4.1**: Guardar las fotos subidas en una carpeta del servidor, con nombres no adivinables (ej. usando un identificador único, no el nombre original del archivo).
    - *Criterio de aceptación*: dos fotos subidas con el mismo nombre original no se sobrescriben ni son accesibles por URL predecible.
16. **Paso 4.2**: Implementar un proceso (manual o programado) que borre fotos con más de N días de antigüedad, conservando solo el resultado ya procesado.
    - *Criterio de aceptación*: ejecutando el proceso de limpieza sobre datos de prueba con fechas antiguas, las fotos correspondientes se eliminan y el resultado asociado permanece intacto.

---

## Fase 5 — Despliegue en internet

17. **Paso 5.1**: Elegir el proveedor de hosting gratuito (Render, Railway o Fly.io) evaluando límites del nivel gratuito vigente al momento de implementar.
    - *Criterio de aceptación*: decisión documentada con la comparación realizada.
18. **Paso 5.2**: Configurar variables de entorno (secretos, configuración de base de datos) en el proveedor elegido, sin incluir secretos en el código fuente.
    - *Criterio de aceptación*: el backend arranca correctamente en el hosting, sin ningún secreto visible en el repositorio de GitHub.
19. **Paso 5.3**: Verificar que el backend desplegado responde correctamente a `GET /health` y `POST /procesar` desde fuera de la red local.
    - *Criterio de aceptación*: una petición realizada desde un dispositivo fuera de la red de tu casa/trabajo obtiene respuesta correcta.

---

## Fase 6 — Frontend web móvil

20. **Paso 6.1**: Crear una página de login simple (HTML/CSS/JS), conectada al endpoint `POST /login`.
    - *Criterio de aceptación*: un usuario de prueba puede iniciar sesión desde el navegador del celular.
21. **Paso 6.2**: Crear la pantalla de selección de examen y lista de alumnos, consumiendo los endpoints correspondientes.
    - *Criterio de aceptación*: tras el login, se listan correctamente los templates y rosters del usuario.
22. **Paso 6.3**: Implementar la captura/subida de foto desde el celular (usando el input nativo de cámara del navegador) y su envío a `POST /procesar`.
    - *Criterio de aceptación*: sacar una foto desde el celular y enviarla devuelve el resultado esperado en pantalla.
23. **Paso 6.4**: Implementar la pantalla de asignación de alumno (lista con detección de "ya asignado") y visualización del resultado final con la hoja marcada.
    - *Criterio de aceptación*: el flujo completo (login → elegir examen → foto → asignar alumno → ver resultado) se completa de punta a punta desde un celular real.
24. **Paso 6.5**: Desplegar el frontend (GitHub Pages, Netlify, o el mismo servicio del backend) y verificar el flujo completo en producción.
    - *Criterio de aceptación*: el flujo completo del Paso 6.4 funciona accediendo por la URL pública, desde un celular distinto al de desarrollo.

---

## Fase 7 — Validación con uso real

25. **Paso 7.1**: Usar el sistema en producción con un examen real (propio o de un colega que acceda a probarlo).
    - *Criterio de aceptación*: se completa la corrección de al menos un curso completo usando únicamente la web móvil desplegada, sin intervención manual en el backend.
26. **Paso 7.2**: Relevar problemas encontrados (de uso, de precisión, de rendimiento) y priorizarlos.
    - *Criterio de aceptación*: lista escrita de issues encontrados, ordenada por impacto.
27. **Paso 7.3**: Resolver los issues críticos antes de considerar el MVP estable.
    - *Criterio de aceptación*: repetir el Paso 7.1 sin encontrar issues críticos nuevos.
