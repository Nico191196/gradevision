import json
import os
import string


def normalizar_nombre(texto):
    """Convierte un texto libre (ej: 'Biología 5to año') en un nombre
    seguro para usar como nombre de archivo (ej: 'biologia_5to_año')."""
    return "".join(c if c.isalnum() else "_" for c in texto.strip().lower())


def pedir_entero(mensaje, minimo=1):
    """Pide un número entero por teclado, repitiendo hasta que sea válido."""
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit() and int(entrada) >= minimo:
            return int(entrada)
        print(f"  Por favor ingresá un número entero de {minimo} o más.")


def crear_template_interactivo(carpeta_salida="assets/templates"):
    print("=== Configuración de la hoja de examen ===\n")
    nombre = input("Nombre del examen/materia (ej: Biología 5to año): ").strip()
    total_preguntas = pedir_entero("¿Cuántas preguntas tiene el examen en total? ")
    opciones = pedir_entero("¿Cuántas opciones de respuesta tiene cada pregunta (A, B, C...)? ", minimo=2)

    while True:
        bloques = pedir_entero("¿En cuántos bloques/columnas está dividida la hoja? ")
        if total_preguntas % bloques == 0:
            break
        print(f"  {total_preguntas} preguntas no se puede dividir en partes iguales entre {bloques} bloques. Probá con otro número.")

    template = {
        "nombre": nombre,
        "total_preguntas": total_preguntas,
        "opciones_por_pregunta": opciones,
        "bloques": bloques
    }

    os.makedirs(carpeta_salida, exist_ok=True)
    nombre_archivo = f"template_{normalizar_nombre(nombre)}.json"
    ruta = os.path.join(carpeta_salida, nombre_archivo)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(template, archivo, ensure_ascii=False, indent=2)

    print(f"\nConfiguración de la hoja guardada en: {ruta}\n")
    return template, ruta


def pedir_clave_respuestas(template):
    total_preguntas = template["total_preguntas"]
    opciones = template["opciones_por_pregunta"]
    letras_validas = string.ascii_uppercase[:opciones]

    print("=== Carga de la clave de respuestas ===\n")
    print(f"Ingresá las {total_preguntas} respuestas correctas, EN ORDEN, una letra por pregunta,")
    print(f"todas juntas y sin espacios (letras válidas: {', '.join(letras_validas)}).")
    print(f"Ejemplo para las primeras preguntas: ABCDABCDAB...\n")

    while True:
        entrada = input(f"Respuestas ({total_preguntas} letras): ").strip().upper()

        if len(entrada) != total_preguntas:
            print(f"  Ingresaste {len(entrada)} letras, pero se esperaban {total_preguntas}. Probá de nuevo.\n")
            continue

        letras_invalidas = sorted(set(c for c in entrada if c not in letras_validas))
        if letras_invalidas:
            print(f"  Encontré letras no válidas: {letras_invalidas}. Solo se permite: {', '.join(letras_validas)}.\n")
            continue

        break

    clave = {str(i + 1): entrada[i] for i in range(total_preguntas)}

    print("\nRevisá la clave antes de guardar:")
    for pregunta, letra in clave.items():
        print(f"  Pregunta {pregunta}: {letra}")

    confirmacion = input("\n¿Es correcta? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("\nCancelado. Volvé a ejecutar el programa para intentar de nuevo.")
        return None

    return clave


def guardar_clave(clave, nombre_examen, carpeta_salida="assets/answer_keys"):
    os.makedirs(carpeta_salida, exist_ok=True)
    nombre_archivo = f"clave_{normalizar_nombre(nombre_examen)}.json"
    ruta = os.path.join(carpeta_salida, nombre_archivo)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(clave, archivo, ensure_ascii=False, indent=2)

    return ruta

def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(datos, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def pedir_entero_opcional(mensaje, valor_actual, minimo=1):
    """
    Igual que pedir_entero, pero si el profesor no escribe nada y
    aprieta Enter, se mantiene el valor actual.
    """
    while True:
        entrada = input(f"{mensaje} (actual: {valor_actual}, Enter para no cambiar): ").strip()
        if entrada == "":
            return valor_actual
        if entrada.isdigit() and int(entrada) >= minimo:
            return int(entrada)
        print(f"  Por favor ingresá un número entero de {minimo} o más, o dejalo vacío.")


def mostrar_detalle_examen(examen):
    template = cargar_json(examen["ruta_template"])
    clave = cargar_json(examen["ruta_clave"])

    print(f"\nNombre: {template['nombre']}")
    print(f"Total de preguntas: {template['total_preguntas']}")
    print(f"Opciones por pregunta: {template['opciones_por_pregunta']}")
    print(f"Bloques: {template['bloques']}")
    print("Clave de respuestas:")
    for pregunta, letra in clave.items():
        print(f"  Pregunta {pregunta}: {letra}")


def editar_examen_interactivo(examen):
    template = cargar_json(examen["ruta_template"])

    print(f"\nEditando: {template['nombre']}")
    print("Dejá vacío (Enter) cualquier campo que no quieras cambiar.\n")

    nuevo_nombre = input(f"Nombre (actual: {template['nombre']}): ").strip()
    if nuevo_nombre != "":
        template["nombre"] = nuevo_nombre

    nuevo_total = pedir_entero_opcional("Total de preguntas", template["total_preguntas"])
    nuevas_opciones = pedir_entero_opcional("Opciones por pregunta", template["opciones_por_pregunta"], minimo=2)

    while True:
        nuevos_bloques = pedir_entero_opcional("Bloques/columnas", template["bloques"])
        if nuevo_total % nuevos_bloques == 0:
            break
        print(f"  {nuevo_total} preguntas no se puede dividir en partes iguales entre {nuevos_bloques} bloques.")

    estructura_cambio = (
        nuevo_total != template["total_preguntas"]
        or nuevas_opciones != template["opciones_por_pregunta"]
    )

    template["total_preguntas"] = nuevo_total
    template["opciones_por_pregunta"] = nuevas_opciones
    template["bloques"] = nuevos_bloques

    guardar_json(template, examen["ruta_template"])
    print(f"\nConfiguración actualizada en: {examen['ruta_template']}")

    if estructura_cambio:
        print("\nComo cambió la cantidad de preguntas o de opciones, hay que volver a cargar la clave de respuestas.")
        clave = pedir_clave_respuestas(template)
        if clave is not None:
            guardar_json(clave, examen["ruta_clave"])
            print(f"Clave actualizada en: {examen['ruta_clave']}")
    else:
        print("\n¿Querés volver a cargar también la clave de respuestas? (s/n): ", end="")
        if input().strip().lower() == "s":
            clave = pedir_clave_respuestas(template)
            if clave is not None:
                guardar_json(clave, examen["ruta_clave"])
                print(f"Clave actualizada en: {examen['ruta_clave']}")


def borrar_examen_interactivo(examen):
    print(f"\nVas a borrar: {examen['nombre']}")
    print(f"  {examen['ruta_template']}")
    print(f"  {examen['ruta_clave']}")
    confirmacion = input("\n¿Confirmás que querés borrarlo? Esta acción no se puede deshacer (s/n): ").strip().lower()

    if confirmacion != "s":
        print("Cancelado, no se borró nada.")
        return

    os.remove(examen["ruta_template"])
    os.remove(examen["ruta_clave"])
    print("Examen borrado correctamente.")