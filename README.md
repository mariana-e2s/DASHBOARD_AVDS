# Fibrive - Aplicação Médica

A **Fibrive** é uma aplicação desenvolvida para apoiar o acompanhamento de pacientes com fibromialgia, permitindo a consulta e análise de dados clínicos através de um dashboard médico.

A aplicação permite ao médico visualizar:

- Dados gerais dos pacientes;
- Gráficos de sono e dor;
- Exercícios concluídos;
- Medicação registada;
- Alertas, metas de saúde e relatórios clínicos.

## Tecnologias usadas

- `streamlit` — interface web do dashboard;
- `firebase-admin` — ligação à Firebase/Firestore;
- `pandas` — tratamento dos dados;
- `plotly` — gráficos do dashboard;
- `reportlab` — geração de relatórios PDF;
- `streamlit-option-menu` — menu lateral personalizado.

## Instalação

Na pasta principal do projeto, executar:

```bash
pip install -r requirements.txt
```

## Executar a aplicação

Na pasta onde está o ficheiro `app.py`, executar:

```bash
py -m streamlit run app.py
```

## Chave de acesso à base de dados

Por segurança, a chave privada da Firebase/Firestore **não está incluída no repositório**.

Sem este ficheiro, a aplicação não consegue estabelecer ligação com a base de dados.

## Repositório

```text
https://github.com/mariana-e2s/DASHBOARD_AVDS.git
```

## Estrutura do projeto

O projeto está organizado em várias pastas principais:

- `app_pages/` — páginas do dashboard, como resumo, pacientes, alertas, metas, mapa corporal e relatórios;
- `components/` — componentes reutilizáveis da interface, como gráficos, layout e cartões de paciente;
- `repositories/` — ficheiros responsáveis por obter dados da Firebase/Firestore;
- `utils/` — funções auxiliares para tratamento de dados e geração de PDFs;
- `flutterflow/` — funções Dart usadas na aplicação mobile desenvolvida em FlutterFlow.

## Modelo relacional da base de dados

A nossa base de dados está formatada de acordo com o seguinte modelo relacional:

![Modelo Relacional](Modelo%20Relacional.png)

## Estrutura geral da base de dados

A aplicação utiliza várias coleções para organizar os dados:

- `User` — dados dos utilizadores/pacientes;
- `Dor` — registos de dor;
- `Sono` — registos de sono;
- `Medicacao` — medicação habitual e SOS;
- `SOS` — contactos de emergência;
- `ExercicioRecomendado` — biblioteca de exercícios;
- `UserExercicio` — exercícios realizados por cada utilizador;
- `GamificacaoUser` — progresso de gamificação.

## Autenticação

O dashboard possui uma página de login reservada ao profissional de saúde.  
Apenas após autenticação o médico consegue aceder aos dados clínicos dos pacientes.
