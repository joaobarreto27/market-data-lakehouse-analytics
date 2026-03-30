"""Base JDBC repository abstractions for query-based data access."""

from abc import ABC, abstractmethod
from typing import Any

from pyspark.sql import DataFrame

from infrastructure.report.utils import PySparkDataReader, SqlQueryLoader


class JdbcQueryRepository(ABC):
    """Abstract base class to support JDBC query operations via Spark."""

    @staticmethod
    def _get_query_loader(sql_file: str, layer: str) -> SqlQueryLoader:
        """Return a SQL loader for provided file and layer."""
        return SqlQueryLoader(sql_file=sql_file, layer=layer)

    def read_from_jdbc(
        self,
        spark_session: Any,
        db_connection: Any,
        sql_file: str,
        layer: str = "gold",
    ) -> DataFrame:
        """Execute a parameterized SQL file through JDBC via Spark DataReader."""
        query_loader = self._get_query_loader(sql_file=sql_file, layer=layer)

        return PySparkDataReader(spark=spark_session).read_from_jdbc(
            query_loader=query_loader,
            db_connection=db_connection,
        )

    @abstractmethod
    def read_default(self, spark_session: Any, db_connection: Any) -> DataFrame:
        """Read the default query for this repository."""
        raise NotImplementedError
