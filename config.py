from pathlib import Path

BASE_DIR = Path(__file__).parent
SERVICE_ACCOUNT_KEY_PATH = BASE_DIR / "serviceAccountKey.json"

# =========================
# COLLECTIONS
# =========================

USER_COLLECTION = "User"
DOR_COLLECTION = "Dor"
SONO_COLLECTION = "Sono"
MEDICACAO_COLLECTION = "Medicacao"
SOS_COLLECTION = "SOS"
EXERCICIO_RECOMENDADO_COLLECTION = "ExercicioRecomendado"
USER_EXERCICIO_COLLECTION = "UserExercicio"
GAMIFICACAO_COLLECTION = "gamificacao"


# =========================
# USER
# =========================

USER_ID_FIELD = "UserID"
USER_NAME_FIELD = "nome"
USER_AGE_FIELD = "idade"
USER_EMAIL_FIELD = "email"
USER_PHOTO_FIELD = "userPhoto"
USER_DISPLAY_NAME_FIELD = "display_name"
USER_PHOTO_URL_FIELD = "photo_url"
USER_UID_FIELD = "uid"
USER_CREATED_TIME_FIELD = "created_time"
USER_PHONE_FIELD = "phone_number"


# =========================
# DOR
# =========================

DOR_ID_FIELD = "dorID"
DOR_LOCALIZACAO_FIELD = "localizacao"
DOR_INTENSIDADE_FIELD = "intensidade"
DOR_NIVEL_FIELD = "nivelDor"
DOR_USER_REFERENCE_FIELD = "UserID"
DOR_DATA_FIELD = "data"


# =========================
# SONO
# =========================

SONO_ID_FIELD = "sonoID"
SONO_QUALIDADE_FIELD = "qualidade"
SONO_HORAS_FIELD = "horasSono"
SONO_DESPERTARES_FIELD = "despertaresNoturnos"
SONO_USER_REFERENCE_FIELD = "UserID"
SONO_DATA_FIELD = "data"


# =========================
# MEDICACAO
# =========================

MEDICACAO_ID_FIELD = "medicacaoID"
MEDICACAO_NOME_FIELD = "nome"
MEDICACAO_TIPO_FIELD = "tipoMedicacao"
MEDICACAO_QUANTIDADE_FIELD = "quantidade"
MEDICACAO_HORARIO_FIELD = "horarioToma"
MEDICACAO_USER_REFERENCE_FIELD = "UserID"


# =========================
# SOS
# =========================

SOS_ID_FIELD = "sosID"
SOS_CONTACTO_FIELD = "contactoSOS"
SOS_USER_REFERENCE_FIELD = "userID"


# =========================
# EXERCICIO RECOMENDADO
# =========================

EXERCICIO_RECOMENDADO_COLLECTION = "ExercicioRecomendado"

EXERCICIO_RECOMENDADO_ID_FIELD = "exercicioRecomendadoID"
EXERCICIO_RECOMENDADO_NOME_FIELD = "nome"
EXERCICIO_RECOMENDADO_DESCRICAO_FIELD = "descricao"
EXERCICIO_RECOMENDADO_NIVEL_DOR_FIELD = "nivelDor"
EXERCICIO_RECOMENDADO_ZONA_DOR_FIELD = "zonaDor"
EXERCICIO_RECOMENDADO_VIDEO_FIELD = "video"


# =========================
# USER EXERCICIO
# =========================

USER_EXERCICIO_COLLECTION = "UserExercicio"

USER_EXERCICIO_ID_FIELD = "UserExercicioID"
USER_EXERCICIO_USER_REFERENCE_FIELD = "UserID"
USER_EXERCICIO_EXERCICIO_REFERENCE_FIELD = "ExercicioID"
USER_EXERCICIO_DATA_FIELD = "data"
USER_EXERCICIO_DIFICULDADE_FIELD = "dificuldade"


# =========================
# GAMIFICACAO
# =========================

GAMIFICACAO_ID_FIELD = "gamificacaoID"
GAMIFICACAO_TUTORIAL_FIELD = "tutorial"