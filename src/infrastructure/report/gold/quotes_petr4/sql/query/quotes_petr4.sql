SELECT
    symbol,
    "regularMarketPrice" AS current_price,
    "regularMarketPreviousClose" AS previous_close,
    ("regularMarketPrice" - "regularMarketPreviousClose") AS price_change,
    ("regularMarketTime"::timestamptz AT TIME ZONE 'America/Sao_Paulo')
        AS market_datetime_sp
FROM public.quotes_petr4
ORDER BY "regularMarketTime" DESC
