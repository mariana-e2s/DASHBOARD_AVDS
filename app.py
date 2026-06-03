import streamlit as st
from pathlib import Path
from streamlit_option_menu import option_menu

from auth import check_authentication, logout_button
from styles import apply_styles

from repositories.user_repository import get_all_users

from app_pages.summary import show_general_summary
from app_pages.patients import show_patients_page
from app_pages.alerts import show_alerts_page
from app_pages.health_goals import show_health_goals_page
from app_pages.body_map import show_body_map_page
from app_pages.reports import show_reports_page


st.set_page_config(
    page_title="DASHBOARD CLÍNICO FIBRIVE",
    page_icon="FIBRIVE_logo.png",
    layout="wide"
)

check_authentication()
apply_styles()

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "FIBRIVE_logo.png"


users = get_all_users()

if not users:
    st.warning("Não existem pacientes na coleção User.")
    st.stop()


if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), width=140)
else:
    st.sidebar.warning("Logo não encontrado.")


with st.sidebar:
    selected_page = option_menu(
        menu_title=None,
        options=[
            "Resumo Geral",
            "Pacientes",
            "Alertas",
            "Metas de Saúde",
            "Mapa Corporal",
            "Relatórios"
        ],
        icons=[
            "bar-chart-line",
            "person",
            "exclamation-triangle",
            "bullseye",
            "person-standing",
            "file-earmark-text"
        ],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#F8FAFC"
            },
            "icon": {
                "color": "#8E7CC3",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "16px",
                "color": "#111827",
                "text-align": "left",
                "margin": "4px 0",
                "border-radius": "12px",
                "padding": "10px 14px",
                "--hover-color": "#F3E8FF",
            },
            "nav-link-selected": {
                "background-color": "#EDE7F6",
                "color": "#111827",
                "font-weight": "700",
            },
        }
    )

    st.markdown("---")
    logout_button()


if selected_page == "Resumo Geral":
    show_general_summary(users)

elif selected_page == "Pacientes":
    show_patients_page(users)

elif selected_page == "Alertas":
    show_alerts_page(users)

elif selected_page == "Metas de Saúde":
    show_health_goals_page(users)

elif selected_page == "Mapa Corporal":
    show_body_map_page(users)

elif selected_page == "Relatórios":
    show_reports_page(users)