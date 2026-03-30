# 📊 Data Engineering Project (English)

## 🚀 Overview

This project demonstrates a complete data pipeline using modern data engineering tools.

## 🧰 Tech Stack

* Python
* PySpark
* SQL
* Apache Airflow
* Docker
* Streamlit

## 📌 Highlights

* Data pipeline orchestration
* Batch processing
* Data transformation and modeling
* Performance optimization
* Interactive dashboard with Streamlit

## 📦 How to run

```bash
# from repository root
python -m pip install -U poetry
poetry install

# start streamlit dashboard
poetry run streamlit run src/infrastructure/report/dashboard/app.py
```

## 🛠 Project structure

* `infrastructure/report/worker` - ETL process
* `infrastructure/report/repository` - repository pattern and data access
* `infrastructure/report/utils` - shared utilities (DB connection, query loading)
* `infrastructure/report/dashboard` - Streamlit dashboard
