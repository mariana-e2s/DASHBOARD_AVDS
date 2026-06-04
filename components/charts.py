import streamlit as st
import pandas as pd
import plotly.express as px

from repositories.sono_repository import get_sono_by_user
from repositories.dor_repository import get_dor_by_user
from repositories.medicacao_repository import get_medicacao_by_user
from repositories.user_exercicio_repository import get_user_exercicios_by_user

from utils.data_utils import to_dataframe


def show_sono_chart(user_doc_ref):
    st.subheader("Sono")

    sono_df = to_dataframe(get_sono_by_user(user_doc_ref))

    if sono_df.empty:
        st.info("Este paciente ainda não tem registos de sono.")
        return

    st.dataframe(sono_df, use_container_width=True)

    if "Horas de Sono" not in sono_df.columns or "Despertares Noturnos" not in sono_df.columns:
        st.info("Os campos necessários para gerar o gráfico de sono não existem nos dados.")
        return

    sono_df["Horas de Sono"] = pd.to_numeric(sono_df["Horas de Sono"], errors="coerce")
    sono_df["Despertares Noturnos"] = pd.to_numeric(sono_df["Despertares Noturnos"], errors="coerce")

    sono_df = sono_df.dropna(subset=["Horas de Sono", "Despertares Noturnos"])

    if sono_df.empty:
        st.info("Não existem valores numéricos suficientes para gerar o gráfico de sono.")
        return

    fig = px.line(
        sono_df,
        x="Horas de Sono",
        y="Despertares Noturnos",
        markers=True,
        title="Relação entre horas de sono e despertares noturnos"
    )

    fig.update_layout(
        xaxis_title="Horas de sono",
        yaxis_title="Despertares noturnos",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(
        line=dict(color="#BFA2DB", width=4),
        marker=dict(color="#8E7CC3", size=10)
    )

    st.plotly_chart(fig, use_container_width=True)


def show_exercicio_chart(user_doc_ref):
    st.subheader("Exercício")

    exercicio_df = to_dataframe(get_user_exercicios_by_user(user_doc_ref))

    if exercicio_df.empty:
        st.info("Este paciente ainda não tem exercícios concluídos.")
        return

    st.dataframe(exercicio_df, use_container_width=True)


def show_dor_chart(user_doc_ref):
    st.subheader("Dor")

    dor_df = to_dataframe(get_dor_by_user(user_doc_ref))

    if dor_df.empty:
        st.info("Este paciente ainda não tem registos de dor.")
        return

    st.dataframe(dor_df, use_container_width=True)

    if "Localização" not in dor_df.columns or "Intensidade" not in dor_df.columns:
        st.info("Os campos necessários para gerar o gráfico de dor não existem nos dados.")
        return

    dor_df["Intensidade"] = pd.to_numeric(dor_df["Intensidade"], errors="coerce")
    dor_df = dor_df.dropna(subset=["Intensidade"])

    if dor_df.empty:
        st.info("Não existem valores numéricos suficientes para gerar o gráfico de dor.")
        return

    fig = px.bar(
        dor_df,
        x="Localização",
        y="Intensidade",
        title="Intensidade da dor por localização"
    )

    fig.update_layout(
        xaxis_title="Localização",
        yaxis_title="Intensidade",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(marker_color="#8E7CC3")

    st.plotly_chart(fig, use_container_width=True)


def show_medicacao_table(user_doc_ref):
    st.subheader("Medicação")

    medicacao_df = to_dataframe(get_medicacao_by_user(user_doc_ref))

    if medicacao_df.empty:
        st.info("Este paciente ainda não tem medicação registada.")
        return

    st.dataframe(medicacao_df, use_container_width=True)


def show_sono_dor_relation(sono_df, dor_df):
    st.subheader("Relação entre sono e dor")

    if sono_df.empty or dor_df.empty:
        st.info("Não existem dados suficientes para relacionar sono e dor.")
        return

    if "Horas de Sono" not in sono_df.columns or "Intensidade" not in dor_df.columns:
        st.info("Os campos necessários para cruzar sono e dor não existem nos dados.")
        return

    min_len = min(len(sono_df), len(dor_df))

    relation_df = pd.DataFrame(
        {
            "Horas de Sono": pd.to_numeric(
                sono_df["Horas de Sono"].head(min_len),
                errors="coerce"
            ),
            "Intensidade da Dor": pd.to_numeric(
                dor_df["Intensidade"].head(min_len),
                errors="coerce"
            ),
        }
    ).dropna()

    if relation_df.empty:
        st.info("Não existem valores numéricos suficientes para gerar o gráfico.")
        return

    fig = px.line(
        relation_df,
        x="Horas de Sono",
        y="Intensidade da Dor",
        markers=True,
        title="Relação entre horas de sono e intensidade da dor"
    )

    fig.update_layout(
        xaxis_title="Horas de sono",
        yaxis_title="Intensidade da dor",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(
        line=dict(color="#BFA2DB", width=4),
        marker=dict(color="#8E7CC3", size=10)
    )

    st.plotly_chart(fig, use_container_width=True)