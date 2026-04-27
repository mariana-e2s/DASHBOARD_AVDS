# FibriVe · Dashboard Clínico

Dashboard Streamlit para acompanhamento clínico de pacientes com fibromialgia.

## Instalação

```bash
pip install -r requirements.txt
```

## Executar

```bash
streamlit run app.py
```

## Funcionalidades

### 📊 KPIs em tempo real
- Dor média (últimos 7 dias) com comparação semanal
- Horas de sono médias
- Nível de stress diário
- Adesão terapêutica (%)
- Despertares noturnos

### 🔔 Alertas Clínicos Automáticos
- **Vermelho**: Crise ativa (dor ≥ 7/10), sono < 5h, adesão baixa
- **Laranja**: Tendência de aumento de dor, sono insuficiente
- **Verde**: Parâmetros estáveis

### 📈 Evolução Temporal
- Gráfico de dor / stress / sono com médias móveis de 7 dias
- Zonas de crise automaticamente sombreadas
- Calendário heatmap de intensidade de dor

### 🗺 Mapa de Dor
- Silhueta corporal com overlay de frequência por zona
- Gráfico de barras de frequência por localização

### 💊 Medicação & Sono
- Timeline de adesão terapêutica com taxa de aderência (%)
- Composição do sono: horas + despertares
- Distribuição do cansaço ao acordar

### 🔗 Correlações
- Scatter plot Dor × Stress com coeficiente de correlação
- Matriz de correlação entre todas as variáveis
- **Índice de Risco de Crise** (previsão simples para próximos 7 dias)

### ⬇ Exportar PDF
- Relatório clínico completo exportável em 1 clique

## Ligação ao Firestore

Para ligar ao Google Firestore real, substitui a função `generate_mock_data()` por:

```python
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def load_patient_data(patient_id: str, days: int = 90):
    cutoff = datetime.now() - timedelta(days=days)
    docs = db.collection("patients").document(patient_id)\
             .collection("daily_records")\
             .where("date", ">=", cutoff)\
             .order_by("date").stream()
    records = [doc.to_dict() for doc in docs]
    return pd.DataFrame(records)
```

Garante que o `serviceAccountKey.json` está no mesmo diretório que o `app.py`.
