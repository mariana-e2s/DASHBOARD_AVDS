import streamlit as st

from repositories.user_repository import get_user_display_name
from utils.data_utils import get_patient_dataframes

from components.layout import show_page_header
from components.patient_components import (
    show_user_info,
    show_patient_status,
    show_patient_summary_cards,
)
from components.charts import (
    show_sono_chart,
    show_exercicio_chart,
    show_dor_chart,
    show_medicacao_table,
    show_sono_dor_relation,
)


def show_patients_page(users):
    show_page_header(
        "Dashboard Clínico FIBRIVE",
        "Monitorização clínica personalizada de pacientes com fibromialgia."
    )

    user_names = [get_user_display_name(user) for user in users]

    selected_user_name = st.sidebar.selectbox(
        "Selecionar paciente",
        user_names
    )

    selected_user = next(
        (user for user in users if get_user_display_name(user) == selected_user_name),
        None
    )

    if selected_user is None:
        st.error("Não foi possível encontrar o paciente selecionado.")
        st.stop()

    user_doc_ref = selected_user["doc_ref"]

    sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

    show_user_info(selected_user)

    show_patient_status(sono_df, dor_df)

    show_patient_summary_cards(sono_df, exercicio_df, dor_df, medicacao_df)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        show_sono_chart(user_doc_ref)

    with col2:
        show_exercicio_chart(user_doc_ref)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        show_dor_chart(user_doc_ref)

    with col4:
        show_medicacao_table(user_doc_ref)

    st.divider()

    show_sono_dor_relation(sono_df, dor_df)