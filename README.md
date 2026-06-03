# Fibrive - Aplicação Médica

A **Fibrive** é uma aplicação desenvolvida para apoiar o acompanhamento de pacientes com fibromialgia, permitindo a consulta e análise de dados clínicos através de um dashboard médico.

A aplicação permite ao médico selecionar um paciente e visualizar:

- Dados gerais do paciente;
- Gráfico de sono;
- Gráfico de exercício;
- Gráfico de dor;
- Tabela de medicação;
- Relatórios clínicos;
- Alertas e metas de saúde.

## Tecnologias e bibliotecas usadas

Este projeto usa as seguintes bibliotecas Python:

- `streamlit` — criação da interface gráfica/web da aplicação;
- `firebase-admin` — ligação entre Python e Firebase/Firestore;
- `pandas` — tratamento e organização dos dados em tabelas;
- `plotly` — criação dos gráficos apresentados no dashboard;
- `reportlab` — geração de relatórios clínicos em PDF;
- `streamlit-option-menu` — criação do menu lateral personalizado.

## Instalação

Antes de executar a aplicação, é necessário instalar todas as dependências do projeto.

Na pasta principal do projeto, executar:

```bash
pip install -r requirements.txt
```

## Executar a aplicação

Para iniciar o dashboard, executar o seguinte comando na pasta onde se encontra o ficheiro `app.py`:

```bash
py -m streamlit run app.py
```

## Chave de acesso à base de dados

Por questões de segurança, a chave privada de ligação à Firebase/Firestore **não está incluída no repositório**.

Sem o ficheiro, a aplicação não conseguirá estabelecer ligação com a base de dados Firebase.
https://github.com/mariana-e2s/DASHBOARD_AVDS.git

## Modelo relacional da base de dados

A nossa base de dados está formatada de acordo com o seguinte modelo relacional:

![Modelo Relacional](Modelo%20Relacional.png)

## Estrutura geral da base de dados

A aplicação utiliza várias coleções/tabelas para organizar os dados dos pacientes:

- `User` — dados gerais dos utilizadores/pacientes;
- `Dor` — registos de dor, intensidade e localização;
- `Sono` — registos de sono e despertares noturnos;
- `Medicacao` — medicação habitual e medicação SOS;
- `SOS` — contactos de emergência;
- `ExercicioRecomendado` — biblioteca de exercícios recomendados;
- `UserExercicio` — exercícios realizados por cada utilizador;
- `Gamificacao` — elementos associados à gamificação.

## Autenticação

O dashboard possui uma página de login reservada ao profissional de saúde.

Apenas após autenticação o médico consegue aceder às páginas do dashboard e consultar os dados clínicos dos pacientes.
