from gradevision_core.templates import template_editor, template_loader


def mostrar_menu_principal():
    print("\n=== Gestión de exámenes ===")
    print("  1. Crear un examen nuevo")
    print("  2. Ver exámenes existentes")
    print("  3. Editar un examen existente")
    print("  4. Borrar un examen")
    print("  5. Salir")


def elegir_examen_de_lista(examenes, accion):
    print(f"\n=== Exámenes disponibles para {accion} ===")
    for i, examen in enumerate(examenes, start=1):
        print(f"  {i}. {examen['nombre']}")

    while True:
        eleccion = input("\nElegí un número (o dejá vacío para cancelar): ").strip()
        if eleccion == "":
            return None
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(examenes):
            return examenes[int(eleccion) - 1]
        print("  Por favor ingresá un número válido de la lista.")


def crear_nuevo():
    template, ruta_template = template_editor.crear_template_interactivo()
    clave = template_editor.pedir_clave_respuestas(template)

    if clave is None:
        return

    ruta_clave = template_editor.guardar_clave(clave, template["nombre"])
    print(f"\nClave de respuestas guardada en: {ruta_clave}")


def main():
    while True:
        mostrar_menu_principal()
        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            crear_nuevo()

        elif opcion == "2":
            examenes = template_loader.listar_examenes_disponibles()
            if not examenes:
                print("\nNo hay ningún examen configurado todavía.")
                continue
            examen = elegir_examen_de_lista(examenes, "ver el detalle")
            if examen:
                template_editor.mostrar_detalle_examen(examen)

        elif opcion == "3":
            examenes = template_loader.listar_examenes_disponibles()
            if not examenes:
                print("\nNo hay ningún examen configurado todavía.")
                continue
            examen = elegir_examen_de_lista(examenes, "editar")
            if examen:
                template_editor.editar_examen_interactivo(examen)

        elif opcion == "4":
            examenes = template_loader.listar_examenes_disponibles()
            if not examenes:
                print("\nNo hay ningún examen configurado todavía.")
                continue
            examen = elegir_examen_de_lista(examenes, "borrar")
            if examen:
                template_editor.borrar_examen_interactivo(examen)

        elif opcion == "5":
            print("\nHasta luego.")
            break

        else:
            print("\nOpción no válida, elegí un número del 1 al 5.")


if __name__ == "__main__":
    main()