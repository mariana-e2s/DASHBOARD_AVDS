import streamlit as st
import pandas as pd
import plotly.express as px

from repositories.user_repository import get_user_display_name
from utils.data_utils import (
    get_patient_dataframes,
    numeric_mean,
    numeric_max,
    numeric_min,
)
from components.layout import show_page_header


def show_general_summary(users):
    show_page_header(
        "Resumo Geral",
        "Visão global dos pacientes acompanhados no dashboard clínico."
    )

    total_pacientes = len(users)
    total_alertas = 0
    pacientes_dor_alta = 0
    pacientes_sono_baixo = 0
    pacientes_sem_registos = 0

    dores = []
    sonos = []

    for user in users:
        user_doc_ref = user["doc_ref"]

        sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

        total_registos = len(sono_df) + len(exercicio_df) + len(dor_df) + len(medicacao_df)

        if total_registos == 0:
            pacientes_sem_registos += 1
            total_alertas += 1

        max_dor = numeric_max(dor_df, "Intensidade")
        min_sono = numeric_min(sono_df, "Horas de Sono")
        media_dor = numeric_mean(dor_df, "Intensidade")
        media_sono = numeric_mean(sono_df, "Horas de Sono")

        if media_dor is not None:
            dores.append(media_dor)

        if media_sono is not None:
            sonos.append(media_sono)

        if max_dor is not None and max_dor >= 8:
            pacientes_dor_alta += 1
            total_alertas += 1

        if min_sono is not None and min_sono < 5:
            pacientes_sono_baixo += 1
            total_alertas += 1

        if medicacao_df.empty:
            total_alertas += 1

    media_geral_dor = sum(dores) / len(dores) if dores else None
    media_geral_sono = sum(sonos) / len(sonos) if sonos else None

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pacientes", total_pacientes)

    with col2:
        st.metric("Alertas ativos", total_alertas)

    with col3:
        st.metric("Dor média geral", f"{media_geral_dor:.1f}/10" if media_geral_dor is not None else "Sem dados")

    with col4:
        st.metric("Sono médio geral", f"{media_geral_sono:.1f} h" if media_geral_sono is not None else "Sem dados")

    st.divider()

    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric("Pacientes com dor elevada", pacientes_dor_alta)

    with col6:
        st.metric("Pacientes com sono baixo", pacientes_sono_baixo)

    with col7:
        st.metric("Pacientes sem registos", pacientes_sem_registos)

    st.divider()

    resumo_df = pd.DataFrame(
        {
            "Indicador": [
                "Total de pacientes",
                "Alertas ativos",
                "Pacientes com dor elevada",
                "Pacientes com sono baixo",
                "Pacientes sem registos",
            ],
            "Valor": [
                total_pacientes,
                total_alertas,
                pacientes_dor_alta,
                pacientes_sono_baixo,
                pacientes_sem_registos,
            ],
        }
    )

    fig = px.bar(
        resumo_df,
        x="Indicador",
        y="Valor",
        title="Resumo de indicadores clínicos"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(marker_color="#BFA2DB")

    st.plotly_chart(fig, use_container_width=True)