import streamlit as st
from pathlib import Path
import base64

BASE_DIR = Path(__file__).parent


def get_logo_path():
    possible_names = [
        "FIBRIVE_logo.png",
    ]

    for name in possible_names:
        path = BASE_DIR / name
        if path.exists():
            return path

    return None


def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def show_login_page():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }

            html, body, .stApp, [data-testid="stAppViewContainer"] {
                background: linear-gradient(
                    180deg,
                    #CDBBFF 0%,
                    #DED5FF 28%,
                    #F4F1FF 58%,
                    #FFFFFF 100%
                ) !important;
                color: #111111 !important;
            }

            [data-testid="stHeader"] {
                background: transparent !important;
            }

            .block-container {
                padding-top: 28px !important;
                max-width: 1100px !important;
            }

            .brand-area {
                text-align: center;
                margin-bottom: 18px;
            }

            .welcome-title {
                text-align: center;
                font-size: 34px;
                font-weight: 800;
                color: #FFFFFF;
                margin-bottom: -4px;
                line-height: 1.1;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.10);
            }

            .logo-wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                margin-top: 0px;
                margin-bottom: 10px;
            }

            .logo-wrapper img {
                width: 320px;
                max-width: 86%;
                display: block;
            }

            .subtitle {
                text-align: center;
                font-size: 18px;
                color: #374151;
                margin-top: 4px;
                margin-bottom: 24px;
            }

            .form-card {
                background-color: rgba(255, 255, 255, 0.92);
                border: 1px solid rgba(255, 255, 255, 0.65);
                border-radius: 18px;
                padding: 28px 30px 24px 30px;
                box-shadow: 0 18px 45px rgba(120, 90, 180, 0.16);
                backdrop-filter: blur(8px);
            }

            label {
                color: #111111 !important;
                font-weight: 600 !important;
                font-size: 15px !important;
            }

            div[data-baseweb="input"] {
                background-color: transparent !important;
            }

            div[data-baseweb="input"] > div {
                background-color: #FFFFFF !important;
                border: 1px solid #D1D5DB !important;
                border-radius: 12px !important;
                min-height: 52px !important;
                color: #111111 !important;
                box-shadow: none !important;
            }

            div[data-baseweb="input"] > div:focus-within {
                border: 1.5px solid #BFA2DB !important;
                box-shadow: 0 0 0 3px rgba(191, 162, 219, 0.22) !important;
            }

            div[data-baseweb="input"] input {
                background-color: #FFFFFF !important;
                color: #111111 !important;
                caret-color: #111111 !important;
                font-size: 16px !important;
            }

            div[data-baseweb="input"] svg {
                color: #6B7280 !important;
                fill: #6B7280 !important;
            }

            div[data-testid="stFormSubmitButton"] {
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                margin-top: 22px !important;
            }

            div[data-testid="stFormSubmitButton"] > button {
                width: 230px !important;
                height: 54px !important;
                border-radius: 14px !important;
                border: none !important;
                background-color: #BFA2DB !important;
                color: white !important;
                font-weight: 700 !important;
                font-size: 17px !important;
                box-shadow: 0 10px 24px rgba(120, 90, 180, 0.28) !important;
                margin: 0 auto !important;
                display: block !important;
            }

            div[data-testid="stFormSubmitButton"] > button:hover {
                background-color: #8E7CC3 !important;
                color: white !important;
                border: none !important;
            }

            .footer-text {
                text-align: center;
                margin-top: 30px;
                font-size: 14px;
                color: #6B7280;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    logo_path = get_logo_path()

    top_col1, top_col2, top_col3 = st.columns([1, 2, 1])

    with top_col2:
        st.markdown("<div class='brand-area'>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="welcome-title">
                Welcome to
            </div>
            """,
            unsafe_allow_html=True
        )

        if logo_path is not None:
            logo_base64 = image_to_base64(logo_path)

            st.markdown(
                f"""
                <div class="logo-wrapper">
                    <img src="data:image/png;base64,{logo_base64}">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="text-align:center; color:#4B5563; margin-bottom:24px;">
                    <br><b>FIBRIVE_logo.png</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="subtitle">
                Dashboard clínico para acompanhamento de pacientes
            </div>
            """,
            unsafe_allow_html=True
        )

    form_col1, form_col2, form_col3 = st.columns([1.15, 2, 1.15])

    with form_col2:
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)

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

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="footer-text">
            Acesso reservado a profissionais autorizados
        </div>
        """,
        unsafe_allow_html=True
    )


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