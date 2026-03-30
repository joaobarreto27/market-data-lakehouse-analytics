"""Module for reading PETR4 data from SQL and JDBC for analytics.

Provides repository class for loading the configured PETR4 SQL query
and executing it against the target database via Spark JDBC.
"""

from pyspark.sql import DataFrame

from infrastructure.report.repository.jdbc_repository import JdbcQueryRepository


class QuotesPetr4GoldQueryRepository(JdbcQueryRepository):
    """Repository for reading PETR4 quotes via Gold query."""

    def read_default(self, spark_session, db_connection) -> DataFrame:
        """Load and execute the configured Gold SQL query via JDBC."""
        return self.read_from_jdbc(
            spark_session=spark_session,
            db_connection=db_connection,
            sql_file="quotes_petr4",
            layer="gold",
        )

    def read_by_action(
        self,
        spark_session,
        db_connection,
        action_name: str,
    ) -> DataFrame:
        """Load and execute an arbitrary SQL file from gold layer by action name."""
        return self.read_from_jdbc(
            spark_session=spark_session,
            db_connection=db_connection,
            sql_file=action_name,
            layer="gold",
        )
