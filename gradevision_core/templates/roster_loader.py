import json
import os
import glob
import difflib


def crear_roster_interactivo(carpeta_salida="assets/rosters"):
    """
    Pide, por teclado, el nombre del curso y la lista de alumnos
    (un nombre por línea, terminando con una línea vacía).
    Guarda el resultado en un archivo JSON.
    """
    print("=== Crear lista de alumnos ===\n")
    nombre_curso = input("Nombre del curso (ej: Biología 5to año): ").strip()

    print("\nEscribí un nombre de alumno por línea.")
    print("Cuando termines, dejá una línea vacía y apretá Enter.\n")

    alumnos = []
    while True:
        nombre = input(f"Alumno {len(alumnos) + 1}: ").strip()
        if nombre == "":
            break
        alumnos.append(nombre)

    if not alumnos:
        print("\nNo se cargó ningún alumno, se cancela la creación de la lista.")
        return None

    os.makedirs(carpeta_salida, exist_ok=True)
    base_nombre = "".join(c if c.isalnum() else "_" for c in nombre_curso.strip().lower())
    ruta = os.path.join(carpeta_salida, f"roster_{base_nombre}.json")

    datos = {"nombre": nombre_curso, "alumnos": alumnos}
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)

    print(f"\nLista de {len(alumnos)} alumnos guardada en: {ruta}")
    return ruta


def listar_rosters(carpeta="assets/rosters"):
    """Devuelve la lista de listas de alumnos disponibles."""
    rutas = glob.glob(os.path.join(carpeta, "roster_*.json"))
    rosters = []
    for ruta in rutas:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        rosters.append({"nombre": datos["nombre"], "alumnos": datos["alumnos"], "ruta": ruta})
    return rosters


def sugerir_nombres(texto_leido, alumnos, cantidad=3):
    """
    Busca, dentro de la lista de alumnos, cuáles nombres se parecen
    más al texto leído por OCR (aunque tenga letras mal leídas),
    usando comparación de similitud de texto.
    Devuelve una lista de hasta 'cantidad' nombres sugeridos, ordenados
    del más parecido al menos parecido.
    """
    if not texto_leido:
        return []
    return difflib.get_close_matches(texto_leido, alumnos, n=cantidad, cutoff=0.3)


def guardar_roster(datos, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def mostrar_detalle_roster(roster):
    print(f"\nCurso: {roster['nombre']}")
    print(f"Cantidad de alumnos: {len(roster['alumnos'])}\n")
    for i, alumno in enumerate(roster["alumnos"], start=1):
        print(f"  {i}. {alumno}")


def editar_roster_interactivo(roster):
    with open(roster["ruta"], "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    while True:
        print(f"\n=== Editando lista: {datos['nombre']} ===")
        for i, alumno in enumerate(datos["alumnos"], start=1):
            print(f"  {i}. {alumno}")

        print("\n  a. Agregar un alumno")
        print("  b. Borrar un alumno")
        print("  c. Cambiar el nombre del curso")
        print("  d. Terminar de editar")

        opcion = input("\nElegí una opción: ").strip().lower()

        if opcion == "a":
            nuevo = input("Nombre del alumno nuevo: ").strip()
            if nuevo:
                datos["alumnos"].append(nuevo)
                print(f"Agregado: {nuevo}")

        elif opcion == "b":
            numero = input("Número del alumno a borrar: ").strip()
            if numero.isdigit() and 1 <= int(numero) <= len(datos["alumnos"]):
                borrado = datos["alumnos"].pop(int(numero) - 1)
                print(f"Borrado: {borrado}")
            else:
                print("Número inválido.")

        elif opcion == "c":
            nuevo_nombre = input(f"Nuevo nombre (actual: {datos['nombre']}): ").strip()
            if nuevo_nombre:
                datos["nombre"] = nuevo_nombre

        elif opcion == "d":
            guardar_roster(datos, roster["ruta"])
            print(f"\nCambios guardados en: {roster['ruta']}")
            break

        else:
            print("Opción no válida.")


def borrar_roster_interactivo(roster):
    print(f"\nVas a borrar la lista: {roster['nombre']} ({len(roster['alumnos'])} alumnos)")
    confirmacion = input("¿Confirmás? Esta acción no se puede deshacer (s/n): ").strip().lower()

    if confirmacion != "s":
        print("Cancelado, no se borró nada.")
        return

    os.remove(roster["ruta"])
    print("Lista borrada correctamente.")