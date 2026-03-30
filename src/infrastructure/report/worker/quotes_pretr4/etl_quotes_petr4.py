"""Daily ETL orchestration pipeline for PETR4 stock quotes.

This module orchestrates the complete ETL (Extract, Transform, Load) process
for PETR4 stock price data across bronze, silver, and gold layers of the
data lake architecture. It manages data ingestion from external APIs,
transformation and validation, and loading into analytics databases.

The pipeline is designed to run on a daily schedule within Apache Airflow,
with comprehensive logging for monitoring and troubleshooting.
"""

import os

from dotenv import load_dotenv
from pyspark.sql import DataFrame

from infrastructure.report.connection.enums.database_enum import DatabaseEnum
from infrastructure.report.connection.enums.sgdb_enum import SgbdEnum
from infrastructure.report.gold.quotes_petr4.query import QuotesPetr4GoldQueryRepository
from infrastructure.report.utils import ConnectionDatabase, SparkSessionManager


def _get_spark_instance(environment: str) -> SparkSessionManager:
    """Get the appropriate Spark session manager for the given environment.

    Selects between SQLite (development) and PostgreSQL (production) based on
    the environment parameter.

    Args:
        environment (str): Environment type ('dev' or 'prd').

    Returns:
        SparkSessionManager: Configured Spark session manager for the environment.
    """
    sgbd_name = (
        SgbdEnum.sqlite.name if environment == "dev" else SgbdEnum.postgresql.name
    )
    return SparkSessionManager(sgbd_name=sgbd_name)


def _get_environment() -> str:
    load_dotenv()
    return os.getenv("ENVIRONMENT", "dev")


def process_gold() -> DataFrame:
    """Execute the configured Gold SQL query and return the result as DataFrame."""
    environment = _get_environment()
    spark = _get_spark_instance(environment)

    sgbd_name = (
        SgbdEnum.sqlite.name if environment == "dev" else SgbdEnum.postgresql.name
    )
    connection = ConnectionDatabase(
        environment=environment,
        db_name=DatabaseEnum.market_data_lakehouse_orchestrator.name,
        sgbd_name=sgbd_name,
    )
    connection.connect_with_retry()

    query_repo = QuotesPetr4GoldQueryRepository()

    try:
        df = query_repo.read_default(
            spark_session=spark,
            db_connection=connection,
        )
        return df
    except Exception as e:
        print("[GOLD_ERROR] Gold query execution failed")
        raise e


if __name__ == "__main__":
    load_dotenv()

    try:
        process_gold()
        print("✅ ETL Pipeline completed successfully!")
    except Exception as e:
        print(f"❌ Error during manual execution: {e}")
