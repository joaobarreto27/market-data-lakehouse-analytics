# 📊 Projeto de Engenharia de Dados (Português)

## 🚀 Visão geral

Este projeto demonstra um pipeline de dados completo usando ferramentas modernas de engenharia de dados.

## 🧰 Stack Tecnológica

* Python
* PySpark
* SQL
* Apache Airflow
* Docker
* Streamlit

## 📌 Destaques

* Orquestração de pipeline de dados
* Processamento em batch
* Transformação e modelagem de dados
* Otimização de desempenho
* Dashboard interativo com Streamlit

## 📦 Como executar

```bash
# na raiz do repositório
python -m pip install -U poetry
poetry install

# iniciar dashboard streamlit
poetry run streamlit run src/infrastructure/report/dashboard/app.py
```

## 🛠 Estrutura do projeto

* `infrastructure/report/worker` - processo de ETL
* `infrastructure/report/repository` - padrão repository e acesso a dados
* `infrastructure/report/utils` - utilitários compartilhados (conexão DB, carregamento SQL)
* `infrastructure/report/dashboard` - dashboard Streamlit
