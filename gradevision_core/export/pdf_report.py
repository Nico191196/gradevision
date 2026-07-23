import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generar_pdf_examen(alumno, resultados, correctas, total, nota, carpeta_salida="resultados/pdf"):
    """
    Genera un PDF individual con el resumen y detalle de un examen.
    Devuelve la ruta del archivo generado.
    """
    os.makedirs(carpeta_salida, exist_ok=True)

    base_nombre = "".join(c if c.isalnum() else "_" for c in alumno)
    ruta = os.path.join(carpeta_salida, f"{base_nombre}.pdf")

    estilos = getSampleStyleSheet()
    documento = SimpleDocTemplate(ruta, pagesize=A4)
    elementos = []

    # --- Encabezado ---
    elementos.append(Paragraph("Resultado de examen - GradeVision", estilos["Title"]))
    elementos.append(Spacer(1, 0.5 * cm))
    elementos.append(Paragraph(f"Alumno/archivo: {alumno}", estilos["Normal"]))
    elementos.append(Paragraph(f"Correctas: {correctas}/{total}", estilos["Normal"]))
    elementos.append(Paragraph(f"Nota: {nota}/10", estilos["Normal"]))
    elementos.append(Spacer(1, 0.7 * cm))

    # --- Tabla de detalle ---
    datos_tabla = [["Pregunta", "Marcó", "Correcta", "Resultado"]]
    for r in resultados:
        estado = "Correcta" if r["es_correcta"] else "Incorrecta"
        datos_tabla.append([str(r["pregunta"]), str(r["marcada"]), str(r["correcta"]), estado])

    tabla = Table(datos_tabla, colWidths=[3 * cm, 3 * cm, 3 * cm, 4 * cm])

    estilo_tabla = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ])

    # Colorear cada fila: verde clarito si es correcta, rojo clarito si no
    for i, r in enumerate(resultados, start=1):
        color = colors.HexColor("#d4edda") if r["es_correcta"] else colors.HexColor("#f8d7da")
        estilo_tabla.add("BACKGROUND", (0, i), (-1, i), color)

    tabla.setStyle(estilo_tabla)
    elementos.append(tabla)

    documento.build(elementos)
    return ruta