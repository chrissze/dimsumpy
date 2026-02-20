


async def get_close(symbol: str) -> float | None:
    """
    DEPENDS: get_time_series_daily
    """
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = await get_time_series_daily(symbol)

    ohlcv_dict: dict[str, dict[str, str]] = data.get('Time Series (Daily)')

    previous_day_quote: dict[str, str] = next(iter(ohlcv_dict.values())) if ohlcv_dict else {}
    
    close_str: str | None = previous_day_quote.get('4. close')
    
    close: float | None = readf(close_str) if close_str else None
    
    return close 




async def get_td_close(symbol: str) -> tuple[datetime.date | None, float | None]:
    """
    DEPENDS: get_time_series_daily
    """
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = await get_time_series_daily(symbol)

    ohlcv_dict: dict[str, dict[str, str]] = data.get('Time Series (Daily)')

    trading_day_str: str | None = next(iter(ohlcv_dict.keys())) if ohlcv_dict else None
    
    td: datetime.date | None = datetime.date.fromisoformat(trading_day_str) if trading_day_str else None
    
    previous_day_quote: dict[str, str] = next(iter(ohlcv_dict.values())) if ohlcv_dict else {}
    
    close_str: str | None = previous_day_quote.get('4. close')
    
    close: float | None = float(close_str) if close_str else None
    
    return td, close 
