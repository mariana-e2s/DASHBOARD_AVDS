from io import BytesIO
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle
    )

    REPORTLAB_AVAILABLE = True

except ImportError:
    REPORTLAB_AVAILABLE = False


def dataframe_to_table_data(df):
    if df.empty:
        return [["Sem dados registados"]]

    table_data = [list(df.columns)]

    for _, row in df.iterrows():
        table_data.append([str(value) for value in row.values])

    return table_data


def add_table_to_pdf(elements, title, df, styles):
    elements.append(Paragraph(title, styles["Heading2"]))
    elements.append(Spacer(1, 0.25 * cm))

    table_data = dataframe_to_table_data(df)

    table = Table(table_data, repeatRows=1)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#BFA2DB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFFFF")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 0.6 * cm))


def generate_patient_pdf_report(
    user,
    user_doc_ref,
    get_user_display_name,
    get_patient_dataframes,
    calculate_patient_status,
    numeric_mean,
    USER_EMAIL_FIELD,
    USER_AGE_FIELD,
    USER_ID_FIELD,
):
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    nome = get_user_display_name(user)
    email = user.get(USER_EMAIL_FIELD, "N/A")

    sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

    status, reason, _ = calculate_patient_status(sono_df, dor_df)

    data_relatorio = datetime.now().strftime("%d/%m/%Y %H:%M")

    elements.append(Paragraph("Relatório Clínico FIBRIVE", styles["Title"]))
    elements.append(Spacer(1, 0.4 * cm))

    elements.append(Paragraph("Dados do paciente", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * cm))

    patient_data = [
        ["Nome", nome],
        ["Email", email],
        ["Estado clínico", status],
        ["Motivo", reason],
        ["Data do relatório", data_relatorio],
    ]

    patient_table = Table(patient_data, colWidths=[4 * cm, 12 * cm])

    patient_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3E8FF")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111111")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(patient_table)
    elements.append(Spacer(1, 0.7 * cm))

    elements.append(Paragraph("Resumo clínico", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * cm))

    media_sono = numeric_mean(sono_df, "Horas de Sono")
    media_qualidade = numeric_mean(sono_df, "Qualidade")
    media_dor = numeric_mean(dor_df, "Intensidade")

    resumo = [
        ["Média de horas de sono", f"{media_sono:.1f} h" if media_sono is not None else "Sem dados"],
        ["Média de qualidade do sono", f"{media_qualidade:.1f}" if media_qualidade is not None else "Sem dados"],
        ["Média de intensidade da dor", f"{media_dor:.1f}/10" if media_dor is not None else "Sem dados"],
        ["Total de exercícios registados", str(len(exercicio_df)) if not exercicio_df.empty else "0"],
        ["Registos de medicação", str(len(medicacao_df)) if not medicacao_df.empty else "0"],
    ]

    resumo_table = Table(resumo, colWidths=[7 * cm, 9 * cm])

    resumo_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F9FAFB")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(resumo_table)
    elements.append(Spacer(1, 0.8 * cm))

    add_table_to_pdf(elements, "Registos de sono", sono_df, styles)
    add_table_to_pdf(elements, "Registos de dor", dor_df, styles)
    add_table_to_pdf(elements, "Registos de exercício", exercicio_df, styles)
    add_table_to_pdf(elements, "Registos de medicação", medicacao_df, styles)

    elements.append(Spacer(1, 0.5 * cm))
    elements.append(
        Paragraph(
            "Relatório gerado automaticamente pelo dashboard clínico FIBRIVE.",
            styles["Normal"]
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf