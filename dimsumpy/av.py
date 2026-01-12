"""


DOCS:
    https://www.alphavantage.co/documentation/


    
NOTES:

- my USD 50 plan is 5 limited at 5 requests per second

- httpx.AsyncClient()'s default timeout is 5 seconds.



"""
# STANDARD LIB
import asyncio

from datetime import date, datetime

from io import StringIO

from pprint import pprint

import os





# THIRD PARTY LIB
import httpx

from httpx import Response

import pandas as pd







def get_cap(symbol: str) -> float | None:
    """
    DEPENDS: get_overview. get_etf_aum
    """
    data: dict[str, str] = get_overview(symbol)   # ETF result will be an empty dict {}

    cap_str: str | None = data.get('MarketCapitalization')

    if cap_str is not None:
        return float(cap_str)
    else:
        return get_etf_aum(symbol)         


async def async_cap(symbol: str) -> float | None:
    """
    DEPENDS: async_overview. async_etf_aum
    """
    data: dict[str, str] = await async_overview(symbol)   # ETF result will be an empty dict {}

    cap_str: str | None = data.get('MarketCapitalization')

    if cap_str is not None:
        return float(cap_str)
    else:
        aum: float | None = await async_etf_aum(symbol)         
        return aum




def get_close(symbol: str) -> float | None:
    """
    DEPENDS: get_time_series_daily
    """
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = get_time_series_daily(symbol)

    ohlcv_dict: dict[str, dict[str, str]] = data.get('Time Series (Daily)')

    previous_day_quote: dict[str, str] = next(iter(ohlcv_dict.values())) if ohlcv_dict else {}
    
    close_str: str | None = previous_day_quote.get('4. close')
    
    close: float | None = float(close_str) if close_str else None
    
    return close 




async def async_close(symbol: str) -> float | None:
    """
    DEPENDS: async_time_series_daily
    """
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = await async_time_series_daily(symbol)

    ohlcv_dict: dict[str, dict[str, str]] = data.get('Time Series (Daily)')

    previous_day_quote: dict[str, str] = next(iter(ohlcv_dict.values())) if ohlcv_dict else {}
    
    close_str: str | None = previous_day_quote.get('4. close')
    
    close: float | None = float(close_str) if close_str else None
    
    return close 







def get_etf_aum(symbol: str) -> float | None:
    """
    DEPENDS: get_etf_profile
    """
    data: dict[str, str | list[dict[str, str]]] = get_etf_profile(symbol)

    aum_str: str | None = data.get('net_assets')

    aum: float | None = float(aum_str) if aum_str else None

    return aum



async def async_etf_aum(symbol: str) -> float | None:
    """
    DEPENDS: async_etf_profile
    """
    data: dict[str, str | list[dict[str, str]]] = await async_etf_profile(symbol)

    aum_str: str | None = data.get('net_assets')

    aum: float | None = float(aum_str) if aum_str else None

    return aum




def get_etf_list() -> list[str]:
    """
    DEPENDS: get_listing_status
    """
    df: pd.DataFrame = get_listing_status()
    etf_symbols: pd.Series = df.loc[df['assetType'].eq('ETF'), 'symbol']
    etf_list: list[str] = etf_symbols.tolist()
    return etf_list



async def async_etf_list() -> list[str]:
    """
    DEPENDS: async_listing_status
    """
    df: pd.DataFrame = await async_listing_status()
    etf_symbols: pd.Series = df.loc[df['assetType'].eq('ETF'), 'symbol']
    etf_list: list[str] = etf_symbols.tolist()
    return etf_list
    


def get_etf_profile(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {'function': 'ETF_PROFILE', 'symbol': symbol, 'apikey': apikey}
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    r.raise_for_status()
    
    data: dict[str, str | list[dict[str, str]]] = r.json()
    
    return data



async def async_etf_profile(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv("AV_API_KEY")

    params: dict[str, str] = {'function': 'ETF_PROFILE', 'symbol': symbol, 'apikey': apikey}

    async with httpx.AsyncClient() as client:
        r = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, str | list[dict[str, str]]] = r.json()

    return data




def get_historical_options(symbol: str, isodate=None, datatype='json', apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **

    # https://www.alphavantage.co/documentation/#historical-options

    # Any date later than 2008-01-01 is accepted. 
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'HISTORICAL_OPTIONS', 
        'symbol': symbol, 
        'datatype': datatype,
        'apikey': apikey,
        }
    
    if isinstance(isodate, str):
        params['date'] = isodate 
    
    elif isinstance(isodate, datetime): 
        params['date'] = isodate.date().isoformat()
    
    elif isinstance(isodate, date):
        params['date'] = isodate.isoformat() 
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    r.raise_for_status()
    data: dict[str, str | list[dict[str, str]]] = r.json()
    
    return data




async def async_historical_options(symbol: str, isodate=None, datatype='json', apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **

    # https://www.alphavantage.co/documentation/#historical-options

    # Any date later than 2008-01-01 is accepted.

    # I must put datetime check before date, as datetime is a subclass of date
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'HISTORICAL_OPTIONS', 
        'symbol': symbol, 
        'datatype': datatype,
        'apikey': apikey,
        }
    
    if isinstance(isodate, str):
        params['date'] = isodate 
    
    elif isinstance(isodate, datetime): 
        params['date'] = isodate.date().isoformat()
    
    elif isinstance(isodate, date):
        params['date'] = isodate.isoformat() 
    
    async with httpx.AsyncClient() as client:
        r: Response = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, str | list[dict[str, str]]] = r.json()

    return data
















def get_listing_status(isodate=None, state='active', apikey=None) -> pd.DataFrame:
    """
    ** INDEPENDENT ENDPOINT **

    # https://www.alphavantage.co/documentation/#listing-status

    # To ensure optimal API response time, this endpoint uses the CSV format which is more memory-efficient than JSON.

    # By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted to query a list of delisted assets.

    # Any YYYY-MM-DD date later than 2010-01-01 is supported.
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'LISTING_STATUS', 
        'state': state, 
        'apikey': apikey
        }
    
    if isinstance(isodate, str):
        params['date'] = isodate 
    elif isinstance(isodate, datetime): 
        params['date'] = isodate.date().isoformat()
    elif isinstance(isodate, date):
        params['date'] = isodate.isoformat() 
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    r.raise_for_status()

    df: pd.DataFrame = pd.read_csv(StringIO(r.text))

    return df


async def async_listing_status(isodate=None, state='active', apikey=None) -> pd.DataFrame:
    """
    ** INDEPENDENT ENDPOINT **

    # To ensure optimal API response time, this endpoint uses the CSV format which is more memory-efficient than JSON.

    # By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted to query a list of delisted assets.

    # Any YYYY-MM-DD date later than 2010-01-01 is supported.
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'LISTING_STATUS', 
        'state': state, 
        'apikey': apikey
        }
    
    if isinstance(isodate, str):
        params['date'] = isodate 
    elif isinstance(isodate, datetime): 
        params['date'] = isodate.date().isoformat()
    elif isinstance(isodate, date):
        params['date'] = isodate.isoformat() 
    
    async with httpx.AsyncClient() as client:
        r: Response = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        df: pd.DataFrame = pd.read_csv(StringIO(r.text))

    return df





def get_option_chain(symbol: str, isodate=None) -> list[dict[str, str]] | None:
    """
    DEPENDS: get_historical_options 
    """
    data: dict[str, str | list[dict[str, str]]] = get_historical_options(symbol=symbol, isodate=isodate)
    
    option_chain: list[dict[str, str]] | None = data.get('data')

    return option_chain


async def async_option_chain(symbol: str, isodate=None) -> list[dict[str, str]] | None:
    """
    DEPENDS: async_historical_options 
    """

    data: dict[str, str | list[dict[str, str]]] = await async_historical_options(symbol=symbol, isodate=isodate)
    
    option_chain: list[dict[str, str]] | None = data.get('data')

    return option_chain







def get_overview(symbol: str, apikey=None) -> dict[str, str]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': apikey}
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)

    r.raise_for_status()
    
    data: dict[str, str] = r.json()
    
    return data



async def async_overview(symbol: str, apikey=None) -> dict[str, str]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv("AV_API_KEY")

    params: dict[str, str] = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': apikey}

    async with httpx.AsyncClient() as client:
        r: Response = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, str] = r.json()

    return data





def get_symbol_search(keywords: str, datatype='json', apikey=None) -> dict[str, list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'SYMBOL_SEARCH', 
        'keywords': keywords, 
        'datatype': datatype, 
        'apikey': apikey
        }
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    r.raise_for_status()
    
    data: dict[str, list[dict[str, str]]] = r.json()
    
    return data





def get_td_close(symbol: str) -> tuple[date | None, float | None]:
    """
    DEPENDS: get_time_series_daily
    """
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = get_time_series_daily(symbol)

    ohlcv_dict: dict[str, dict[str, str]] = data.get('Time Series (Daily)')

    trading_day_str: str | None = next(iter(ohlcv_dict.keys())) if ohlcv_dict else None
    
    td: date | None = date.fromisoformat(trading_day_str) if trading_day_str else None
    
    previous_day_quote: dict[str, str] = next(iter(ohlcv_dict.values())) if ohlcv_dict else {}
    
    close_str: str | None = previous_day_quote.get('4. close')
    
    close: float | None = float(close_str) if close_str else None
    
    return td, close 




async def async_td_close(symbol: str) -> tuple[date | None, float | None]:
    """
    DEPENDS: async_time_series_daily
    """
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = await async_time_series_daily(symbol)

    ohlcv_dict: dict[str, dict[str, str]] = data.get('Time Series (Daily)')

    trading_day_str: str | None = next(iter(ohlcv_dict.keys())) if ohlcv_dict else None
    
    td: date | None = date.fromisoformat(trading_day_str) if trading_day_str else None
    
    previous_day_quote: dict[str, str] = next(iter(ohlcv_dict.values())) if ohlcv_dict else {}
    
    close_str: str | None = previous_day_quote.get('4. close')
    
    close: float | None = float(close_str) if close_str else None
    
    return td, close 





def get_time_series_daily(symbol: str, outputsize='compact', datatype='json', apikey=None) -> dict[str, dict[str, str] | dict[str, dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'TIME_SERIES_DAILY', 
        'symbol': symbol, 
        'outputsize': outputsize,
        'datatype': datatype,
        'apikey': apikey,
        }
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = r.json()
    
    return data




async def async_time_series_daily(symbol: str, outputsize='compact', datatype='json', apikey=None) -> dict[str, dict[str, str] | dict[str, dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'TIME_SERIES_DAILY', 
        'symbol': symbol, 
        'outputsize': outputsize,
        'datatype': datatype,
        'apikey': apikey,
        }
    
    async with httpx.AsyncClient() as client:
        r: Response = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = r.json()
    
    return data




async def main() -> None:
    td, p = await async_td_close('TSM')
    print(td, p)
    
    # x1, x2 = await asyncio.gather(
    #     async_listing_status(),
    #     async_option_chain('SPY'),
    # )

    # print(x1, x2)


if __name__ == '__main__':
    
    asyncio.run(main())
    
    #td, p = get_td_close('AMD')
    
    #print(type(td), p)
    