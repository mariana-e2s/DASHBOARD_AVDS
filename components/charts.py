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

    fig = px.scatter(
        sono_df,
        x="Horas de Sono",
        y="Despertares Noturnos",
        size="Despertares Noturnos",
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
        marker=dict(color="#8E7CC3", size=12)
    )

    st.plotly_chart(fig, use_container_width=True)


def show_exercicio_chart(user_doc_ref):
    st.subheader("Exercício")

    exercicio_df = to_dataframe(get_user_exercicios_by_user(user_doc_ref))

    if exercicio_df.empty:
        st.info("Este paciente ainda não tem exercícios associados.")
        return

    st.dataframe(exercicio_df, use_container_width=True)

    if "Dificuldade" not in exercicio_df.columns or "Qualidade de Execução" not in exercicio_df.columns:
        st.info("Ainda não existem dados suficientes para gerar o gráfico de exercício.")
        return

    fig = px.bar(
        exercicio_df,
        x="Dificuldade",
        y="Qualidade de Execução",
        title="Qualidade de execução por dificuldade"
    )

    fig.update_layout(
        xaxis_title="Dificuldade",
        yaxis_title="Qualidade de execução",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(marker_color="#BFA2DB")

    st.plotly_chart(fig, use_container_width=True)


def show_dor_chart(user_doc_ref):
    st.subheader("Dor")

    dor_df = to_dataframe(get_dor_by_user(user_doc_ref))

    if dor_df.empty:
        st.info("Este paciente ainda não tem registos de dor.")
        return

    st.dataframe(dor_df, use_container_width=True)

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
            "Horas de Sono": pd.to_numeric(sono_df["Horas de Sono"].head(min_len), errors="coerce"),
            "Intensidade da Dor": pd.to_numeric(dor_df["Intensidade"].head(min_len), errors="coerce"),
        }
    ).dropna()

    if relation_df.empty:
        st.info("Não existem valores numéricos suficientes para gerar o gráfico.")
        return

    fig = px.scatter(
        relation_df,
        x="Horas de Sono",
        y="Intensidade da Dor",
        title="Relação entre horas de sono e intensidade da dor"
    )

    fig.update_layout(
        xaxis_title="Horas de sono",
        yaxis_title="Intensidade da dor",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(marker=dict(color="#8E7CC3", size=10))

    st.plotly_chart(fig, use_container_width=True)