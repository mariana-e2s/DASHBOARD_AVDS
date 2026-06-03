import streamlit as st

from repositories.user_repository import get_user_display_name
from utils.data_utils import (
    get_patient_dataframes,
    numeric_max,
    numeric_min,
)
from components.layout import show_page_header


def show_alerts_page(users):
    show_page_header(
        "Alertas Clínicos",
        "Monitorização de situações que exigem maior atenção clínica."
    )

    alerts_found = False

    total_alertas = 0
    total_dor_alta = 0
    total_sono_baixo = 0
    total_sem_registos = 0
    total_sem_medicacao = 0

    alertas = []

    for user in users:
        nome = get_user_display_name(user)
        user_doc_ref = user["doc_ref"]

        sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

        if dor_df.empty and sono_df.empty and medicacao_df.empty and exercicio_df.empty:
            alerts_found = True
            total_alertas += 1
            total_sem_registos += 1
            alertas.append(("warning", nome, "Sem registos clínicos disponíveis."))
            continue

        max_dor = numeric_max(dor_df, "Intensidade")
        min_sono = numeric_min(sono_df, "Horas de Sono")

        if max_dor is not None and max_dor >= 8:
            alerts_found = True
            total_alertas += 1
            total_dor_alta += 1
            alertas.append(("error", nome, f"Dor elevada registada. Intensidade máxima: {max_dor}/10."))

        if min_sono is not None and min_sono < 5:
            alerts_found = True
            total_alertas += 1
            total_sono_baixo += 1
            alertas.append(("warning", nome, f"Sono insuficiente registado. Valor mínimo: {min_sono} horas."))

        if medicacao_df.empty:
            alerts_found = True
            total_alertas += 1
            total_sem_medicacao += 1
            alertas.append(("info", nome, "Sem registos de medicação."))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de alertas", total_alertas)

    with col2:
        st.metric("Dor elevada", total_dor_alta)

    with col3:
        st.metric("Sono baixo", total_sono_baixo)

    with col4:
        st.metric("Sem medicação", total_sem_medicacao)

    st.divider()

    if not alerts_found:
        st.success("Não existem alertas clínicos relevantes de momento.")
        return

    for tipo, nome, mensagem in alertas:
        texto = f"**{nome}** — {mensagem}"

        if tipo == "error":
            st.error(texto)
        elif tipo == "warning":
            st.warning(texto)
        else:
            st.info(texto)