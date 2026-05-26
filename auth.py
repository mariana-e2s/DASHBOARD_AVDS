import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent


def get_logo_path():
    possible_names = [
        "FIBRIVE_logo.png",
        "logo_fibrive.png",
        "fibrive_logo.png",
        "logo.png"
    ]

    for name in possible_names:
        path = BASE_DIR / name
        if path.exists():
            return path

    return None


def show_login_page():
    st.markdown(
        """
        <style>
            /* Esconder a sidebar na página de login */
            [data-testid="stSidebar"] {
                display: none;
            }

            /* Fundo totalmente branco */
            html, body, .stApp, [data-testid="stAppViewContainer"] {
                background-color: #FFFFFF !important;
                color: #111111 !important;
            }

            [data-testid="stHeader"] {
                background-color: #FFFFFF !important;
            }

            .block-container {
                padding-top: 70px;
                max-width: 850px;
            }

            /* Card principal */
            .login-card {
                background-color: #FFFFFF !important;
                padding: 40px 44px;
                border-radius: 26px;
                border: 1px solid #E5E7EB;
                box-shadow: 0 18px 45px rgba(0, 0, 0, 0.08);
            }

            /* Logo */
            .logo-area {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 28px;
            }

            .logo-shadow {
                display: inline-block;
                padding: 16px 24px;
                border-radius: 24px;
                background-color: #FFFFFF;
                box-shadow: 0 14px 36px rgba(0, 0, 0, 0.10);
            }

            /* Subtítulo */
            .subtitle {
                text-align: center;
                font-size: 17px;
                color: #4B5563;
                margin-bottom: 34px;
            }

            /* Labels */
            label {
                color: #111111 !important;
                font-weight: 600 !important;
            }

            /* Inputs */
            div[data-baseweb="input"] {
                background-color: transparent !important;
            }

            div[data-baseweb="input"] > div {
                background-color: #FFFFFF !important;
                border: 2px solid #111111 !important;
                border-radius: 12px !important;
                color: #111111 !important;
            }

            div[data-baseweb="input"] input {
                background-color: #FFFFFF !important;
                color: #111111 !important;
                caret-color: #111111 !important;
            }

            div[data-baseweb="input"] svg {
                color: #111111 !important;
                fill: #111111 !important;
            }

            /* Botão centrado */
            div[data-testid="stFormSubmitButton"] {
                display: flex;
                justify-content: center;
                margin-top: 18px;
            }

            div[data-testid="stFormSubmitButton"] > button {
                width: 220px;
                height: 52px;
                border-radius: 12px;
                border: none;
                background-color: #BFA2DB;
                color: white !important;
                font-weight: 700;
                font-size: 16px;
                box-shadow: 0 8px 22px rgba(191, 162, 219, 0.45);
            }

            div[data-testid="stFormSubmitButton"] > button:hover {
                background-color: #8E7CC3;
                color: white !important;
                border: none;
            }

            .footer-text {
                text-align: center;
                margin-top: 28px;
                font-size: 13px;
                color: #6B7280;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    logo_path = get_logo_path()

    col1, col2, col3 = st.columns([1, 1.35, 1])

    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)

        if logo_path is not None:
            st.markdown("<div class='logo-area'>", unsafe_allow_html=True)
            st.markdown("<div class='logo-shadow'>", unsafe_allow_html=True)

            st.image(str(logo_path), width=240)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div style="text-align:center; color:#4B5563; margin-bottom:24px;">
                    Coloca o logo na mesma pasta do <b>app.py</b> com o nome:
                    <br><b>FIBRIVE_logo.png</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            """
            <div class="subtitle">
                Dashboard clínico para acompanhamento de pacientes
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            username = st.text_input("Utilizador")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Iniciar sessão")

            if submitted:
                if username == "admin" and password == "fibrive2026":
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Utilizador ou password incorretos.")

        st.markdown(
            """
            <div class="footer-text">
                Acesso reservado a profissionais autorizados
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)


def check_authentication():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        show_login_page()
        st.stop()


def logout_button():
    if st.sidebar.button("Terminar sessão"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()