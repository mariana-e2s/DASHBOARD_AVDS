import streamlit as st

from repositories.user_repository import get_user_display_name
from utils.data_utils import (
    get_patient_dataframes,
    calculate_patient_status,
    numeric_mean,
)
from utils.pdf_utils import (
    REPORTLAB_AVAILABLE,
    generate_patient_pdf_report,
)
from components.layout import show_page_header
from components.patient_components import show_user_info

from config import (
    USER_ID_FIELD,
    USER_AGE_FIELD,
    USER_EMAIL_FIELD,
)


def show_reports_page(users):
    show_page_header(
        "Relatórios",
        "Geração de relatórios clínicos em PDF por paciente."
    )

    if not REPORTLAB_AVAILABLE:
        st.error("A biblioteca reportlab não está instalada. Executa: py -m pip install reportlab")
        return

    user_names = [get_user_display_name(user) for user in users]

    selected_user_name = st.selectbox(
        "Selecionar paciente para relatório",
        user_names,
        key="reports_patient_select"
    )

    selected_user = next(
        (user for user in users if get_user_display_name(user) == selected_user_name),
        None
    )

    if selected_user is None:
        st.error("Não foi possível encontrar o paciente selecionado.")
        return

    user_doc_ref = selected_user["doc_ref"]

    show_user_info(selected_user)

    pdf_report = generate_patient_pdf_report(
        user=selected_user,
        user_doc_ref=user_doc_ref,
        get_user_display_name=get_user_display_name,
        get_patient_dataframes=get_patient_dataframes,
        calculate_patient_status=calculate_patient_status,
        numeric_mean=numeric_mean,
        USER_EMAIL_FIELD=USER_EMAIL_FIELD,
        USER_AGE_FIELD=USER_AGE_FIELD,
        USER_ID_FIELD=USER_ID_FIELD,
    )

    if pdf_report is not None:
        st.download_button(
            label="Exportar relatório PDF",
            data=pdf_report,
            file_name=f"relatorio_fibrive_{get_user_display_name(selected_user).replace(' ', '_')}.pdf",
            mime="application/pdf"
        )