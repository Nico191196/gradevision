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