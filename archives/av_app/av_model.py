


#########################
### GENERAL FUNCTIONS ###
#########################




async def get_cap_aum(symbol: str) -> float | None:
    """
    DEPENDS: get_cap, get_etf_aum
    """
    cap: float | None = await get_cap(symbol)   # ETF result will be an empty dict {}

    if cap is not None:
        return cap
    else:
        aum = await get_etf_aum(symbol)         
        return aum



async def get_etf_list() -> list[str]:
    """
    DEPENDS: get_listing_status
    """
    df: pd.DataFrame = await get_listing_status()
    etf_symbols: pd.Series = df.loc[df['assetType'].eq('ETF'), 'symbol']
    etf_list: list[str] = etf_symbols.tolist()
    return etf_list
    



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

### END OF GENERAL FUNCTIONS ###