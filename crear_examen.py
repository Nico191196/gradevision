import os
from gradevision_core.templates import template_editor


def main():
    template, ruta_template = template_editor.crear_template_interactivo()
    clave = template_editor.pedir_clave_respuestas(template)

    if clave is None:
        return

    ruta_clave = template_editor.guardar_clave(clave, template["nombre"])

    print(f"\nClave de respuestas guardada en: {ruta_clave}")
    print("\nPara corregir con esta configuración, actualizá estas 2 líneas en main.py:")
    print(f'    template = template_loader.cargar_template("{ruta_template.replace(os.sep, "/")}")')
    print(f'    clave = answer_key.cargar_clave("{ruta_clave.replace(os.sep, "/")}")')


if __name__ == "__main__":
    main()