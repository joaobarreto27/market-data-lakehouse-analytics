"""Streamlit dashboard for market data lakehouse reports."""

from typing import Optional

import pandas as pd
import streamlit as st

from infrastructure.report.worker.quotes_pretr4.etl_quotes_petr4 import process_gold


@st.cache_data(ttl=300)
def load_quotes_data() -> Optional[pd.DataFrame]:
    """Load quote data from the ETL gold process and convert to pandas."""
    try:
        df = process_gold()

        if df is None:
            return None

        if hasattr(df, "toPandas"):
            return df.toPandas()

        if isinstance(df, pd.DataFrame):
            return df

        if isinstance(df, (list, dict)):
            return pd.DataFrame(df)

        raise TypeError("Unsupported data type from process_gold: %s" % type(df))

    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None


def run_dashboard() -> None:
    """Run Streamlit dashboard UI."""
    st.set_page_config(
        page_title="Dados de Mercado",
        page_icon="📈",
        layout="wide",
    )

    st.title("📊 Dados de Mercado da Lakehouse")

    df = load_quotes_data()

    if df is None or df.empty:
        st.warning(
            "Nenhum dado carregado ainda. Verifique a execução do ETL "
            "ou a conexão com o banco."
        )
        return

    df.columns = [str(c).strip() for c in df.columns]

    symbol_options = (
        sorted(df["symbol"].dropna().unique()) if "symbol" in df.columns else []
    )

    selected_symbols = st.multiselect(
        "Selecione Ações para Visualizar",
        options=symbol_options,
        default=symbol_options,
    )

    if selected_symbols:
        filtered = df[df["symbol"].isin(selected_symbols)]
    else:
        filtered = df.copy()

    if "market_datetime_sp" in filtered.columns:
        filtered["market_datetime_sp"] = pd.to_datetime(
            filtered["market_datetime_sp"], errors="coerce"
        )

    st.subheader("Indicadores de Mercado")
    if "market_datetime_sp" in filtered.columns:
        latest = (
            filtered.sort_values("market_datetime_sp", ascending=False)
            .groupby("symbol")
            .head(1)
        )
    else:
        latest = filtered

    cols = st.columns(4)
    with cols[0]:
        st.metric("Ações", len(symbol_options))
    with cols[1]:
        st.metric("Linhas", len(filtered))
    with cols[2]:
        if not latest.empty and "current_price" in latest.columns:
            st.metric("Preço Médio Atual", f"{latest['current_price'].mean():.2f}")
        else:
            st.metric("Preço Médio Atual", "N/A")

    with cols[3]:
        if not latest.empty and "price_change" in latest.columns:
            st.metric("Mudança Média de Preço", f"{latest['price_change'].mean():.4f}")
        else:
            st.metric("Mudança Média de Preço", "N/A")

    # Chart
    st.subheader("Preço Histórico")
    if "market_datetime_sp" in filtered.columns:
        chart_df = filtered.sort_values("market_datetime_sp")

        for symbol in selected_symbols:
            series = chart_df[chart_df["symbol"] == symbol]
            st.line_chart(
                series.set_index("market_datetime_sp")["current_price"],
                height=320,
                width=1100,
            )
    else:
        st.info(
            "Data does not have 'market_datetime_sp' column Unable to plot time series."
        )

    # Data summary
    st.subheader("Dados Detalhados")
    filtered_data = filtered.rename(
        columns={
            "symbol": "Símbolo",
            "current_price": "Preço Atual",
            "previous_close": "Fechamento Anterior",
            "price_change": "Variação de Preço",
            "market_datetime_sp": "Data/Hora (SP)",
        }
    )
    st.dataframe(filtered_data.reset_index(drop=True))


if __name__ == "__main__":
    run_dashboard()
