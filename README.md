# Fibrive - Aplicação Médica

A **Fibrive** é uma aplicação que permite ajudar pacientes com fibromialgia, permitir a consulta de dados médicos de pacientes.

A aplicação permite ao médico selecionar um paciente e visualizar:
- Dados gerais do paciente;
- Gráfico de sono;
- Gráfico de exercício;
- Gráfico de dor;
- Tabela de medicação.

## Tecnologias e bibliotecas usadas

Este projeto usa as seguintes bibliotecas Python:

- `streamlit` — criação da interface gráfica/web da aplicação;
- `firebase-admin` — ligação entre Python e Firebase/Firestore;
- `pandas` — tratamento e organização dos dados em tabelas;
- `plotly` — criação dos gráficos apresentados no dashboard.

## Instalação

Antes de executar a aplicação, é necessário instalar todas as dependências do projeto.

Na pasta principal do projeto, executar:

```bash
pip install -r requirements.txt