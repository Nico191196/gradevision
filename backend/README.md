# GradeVision Backend

## Instalación

Con el entorno virtual activado, parado en la **raíz** del repositorio (no en `backend/`):
pip install -e ".[backend]"
Esto instala `gradevision_core` en modo editable junto con las dependencias
del backend (FastAPI, Uvicorn, etc.). No hace falta un `requirements.txt`
separado: `pyproject.toml` es la única fuente de verdad de las dependencias
del proyecto (ver extra `[backend]`).

> Nota: al momento de esta actualización, `backend/` todavía no tiene
> código de aplicación (endpoints). Ver `docs/roadmap.md`, Fase 1.