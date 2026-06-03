import streamlit as st

from repositories.user_repository import get_user_display_name
from utils.data_utils import get_patient_dataframes, numeric_mean
from components.layout import show_page_header


def get_goal_status_badge(progress):
    percentage = int(progress * 100)

    if progress >= 1:
        return """
        <span style="
            background-color: #D1FAE5;
            color: #065F46;
            border: 1.5px solid #8B5CF6;
            border-radius: 12px;
            padding: 6px 14px;
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            display: inline-block;
        ">
            feito
        </span>
        """

    return f"""
    <span style="
        background-color: #F8DED6;
        color: #374151;
        border: 1px solid #E8B8A8;
        border-radius: 12px;
        padding: 6px 14px;
        font-size: 14px;
        font-weight: 500;
        white-space: nowrap;
        display: inline-block;
    ">
        {percentage}% concluído
    </span>
    """


def show_health_goals_page(users):
    show_page_header(
        "Metas de Saúde",
        "Acompanhamento de metas clínicas associadas ao sono, dor, exercício e monitorização."
    )

    user_names = [get_user_display_name(user) for user in users]

    selected_user_name = st.selectbox(
        "Selecionar paciente",
        user_names,
        key="goals_patient_select"
    )

    selected_user = next(
        (user for user in users if get_user_display_name(user) == selected_user_name),
        None
    )

    if selected_user is None:
        st.error("Não foi possível encontrar o paciente selecionado.")
        return

    user_doc_ref = selected_user["doc_ref"]

    sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

    media_sono = numeric_mean(sono_df, "Horas de Sono")
    media_dor = numeric_mean(dor_df, "Intensidade")

    total_exercicios = len(exercicio_df) if not exercicio_df.empty else 0
    total_medicacao = len(medicacao_df) if not medicacao_df.empty else 0
    total_registos = len(sono_df) + len(exercicio_df) + len(dor_df) + len(medicacao_df)

    st.subheader(f"Metas de {get_user_display_name(selected_user)}")

    if media_dor is not None:
        if media_dor < 5:
            dor_progress = 1.0
        else:
            dor_progress = max(0.0, min((10 - media_dor) / 5, 0.9))
    else:
        dor_progress = 0.0

    goals = [
        {
            "title": "Sono adequado",
            "description": "Objetivo: média de sono igual ou superior a 7 horas.",
            "progress": min((media_sono or 0) / 7, 1.0),
            "value": f"{media_sono:.1f} h" if media_sono is not None else "Sem dados",
        },
        {
            "title": "Controlo da dor",
            "description": "Objetivo: manter a dor média abaixo de 5/10.",
            "progress": dor_progress,
            "value": f"{media_dor:.1f}/10" if media_dor is not None else "Sem dados",
        },
        {
            "title": "Exercício físico",
            "description": "Objetivo: pelo menos 3 exercícios ou sessões registadas.",
            "progress": min(total_exercicios / 3, 1.0),
            "value": f"{total_exercicios} exercícios",
        },
        {
            "title": "Monitorização regular",
            "description": "Objetivo: ter pelo menos 7 registos clínicos no total.",
            "progress": min(total_registos / 7, 1.0),
            "value": f"{total_registos} registos",
        },
        {
            "title": "Registo de medicação",
            "description": "Objetivo: existir pelo menos 1 registo de medicação associado ao paciente.",
            "progress": 1.0 if total_medicacao > 0 else 0.0,
            "value": f"{total_medicacao} registos",
        },
    ]

    for goal in goals:
        progress = max(0, min(goal["progress"], 1))
        badge = get_goal_status_badge(progress)

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### {goal['title']}")
                st.markdown(goal["description"])
                st.markdown(f"**Estado atual:** {goal['value']}")

            with col2:
                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                st.markdown(badge, unsafe_allow_html=True)