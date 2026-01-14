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

import requests




def get_shares(symbol: str) -> dict[str, float]:
    
    data: dict[str, str | list[dict[str, str]]] = get_balance_sheet(symbol)
    
    reports: list[dict[str, str]] | None = data.get('quarterlyReports')
    
    share_dict = {}
    
    for x in reports:
        isodate = x['fiscalDateEnding']
        share_dict[isodate] = float(x['commonStockSharesOutstanding'])
    
    return share_dict



def get_balance_sheet(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    
    {
    'symbol':'AMD',
    'annualReports':[
        {
        'fiscalDateEnding': '2024-12-31',
        'commonStockSharesOutstanding': '1637000000'
        }
        ],
    'quarterlyReports':[{
        'fiscalDateEnding': '2025-09-30',
        'commonStockSharesOutstanding': '1641000000'
        }]    
    }
    
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {'function': 'BALANCE_SHEET', 'symbol': symbol, 'apikey': apikey}
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    r.raise_for_status()
    
    data: dict[str, str | list[dict[str, str]]] = r.json()
    
    return data



async def async_balance_sheet(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv("AV_API_KEY")

    params: dict[str, str] = {'function': 'BALANCE_SHEET', 'symbol': symbol, 'apikey': apikey}

    async with httpx.AsyncClient() as client:
        r = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, str | list[dict[str, str]]] = r.json()

    return data



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





def get_income_statement(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    
    {
    'symbol':'AMD',
    'annualReports':[{}],
    'quarterlyReports':[{}]    
    }
    
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {'function': 'INCOME_STATEMENT', 'symbol': symbol, 'apikey': apikey}
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    r.raise_for_status()
    
    data: dict[str, str | list[dict[str, str]]] = r.json()
    
    return data



async def async_income_statement(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv("AV_API_KEY")

    params: dict[str, str] = {'function': 'INCOME_STATEMENT', 'symbol': symbol, 'apikey': apikey}

    async with httpx.AsyncClient() as client:
        r = await client.get('https://www.alphavantage.co/query', params=params)
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



def get_shares_outstanding(symbol: str, datatype='json', apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    
    data is not up to date, about 12-month old.
    
    {    
    'symbol': 'NVDA',
    'status': 'success',
    'data': [{'date': '2025-04-27', 'shares_outstanding_basic': '24441000000', 'shares_outstanding_diluted': '24611000000'}, ...]
    }
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'SHARES_OUTSTANDING',     # Required 
        'symbol': symbol,                     # Required
        'datatype': datatype,                 # Optional
        'apikey': apikey                      # Required
        }
    
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    r.raise_for_status()
    data: dict[str, str | list[dict[str, str]]] = r.json()    
    return data




async def async_shares_outstanding(symbol: str, datatype='json', apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    
    data is not up to date, about 12-month old.
    
    {    
    'symbol': 'NVDA',
    'status': 'success',
    'data': [{'date': '2025-04-27', 'shares_outstanding_basic': '24441000000', 'shares_outstanding_diluted': '24611000000'}, ...]
    }
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'SHARES_OUTSTANDING',     # Required 
        'symbol': symbol,                     # Required
        'datatype': datatype,                 # Optional
        'apikey': apikey                      # Required
        }
    
    async with httpx.AsyncClient() as client:
        r: Response = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, str | list[dict[str, str]]] = r.json()    
    
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





def get_time_series_daily_adjusted(symbol: str, outputsize='compact', datatype='json', apikey=None) -> dict[str, dict[str, str] | dict[str, dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    
    {
    'Meta Data': {}, 
    'Time Series (Daily)': {}
    
    }
    
    
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED', 
        'symbol': symbol,            # Required
        'outputsize': outputsize,    # Optional
        'datatype': datatype,        # Optional
        'apikey': apikey,            # Required
        }
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = r.json()
    
    return data



async def async_time_series_daily_adjusted(symbol: str, outputsize='compact', datatype='json', apikey=None) -> dict[str, dict[str, str] | dict[str, dict[str, str]]]:
    """
    ** INDEPENDENT ENDPOINT **
    """
    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED', 
        'symbol': symbol,           # Required
        'outputsize': outputsize,   # Optional
        'datatype': datatype,       # Optional
        'apikey': apikey,           # Required
        }
    
    async with httpx.AsyncClient() as client:
        r: Response = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = r.json()
    
    return data







def get_prices(symbol: str) -> dict[str, dict[str, str | float | date | None]]:
                                   
    data: dict[str, dict[str, str] | dict[str, dict[str, str]]] = get_time_series_daily_adjusted(symbol, outputsize='full')

    daily_dict: dict[str, dict[str, str]] = data.get('Time Series (Daily)')
    
    final_dict: dict[str, dict[str, str | float | date | None]] = {}
    
    # k is an isodate string like '2022-01-22'
    for k_isodate, v in daily_dict.items():
        price_dict = {}
        
        price_dict['symbol'] = symbol
        price_dict['td'] = date.fromisoformat(k_isodate)
        price_dict['close'] = float(v.get('4. close'))
        price_dict['adjclose'] = float(v.get('5. adjusted close'))
        final_dict[k_isodate] = price_dict 
    
    return final_dict



def get_caps_shares(symbol: str) -> dict[str, dict[str, str | float | date | None]]:
    """
    
    x = get_closes_and_caps('AMD')
    data = list(x.values())
    pprint(data[:140], sort_dicts=False)
    
    """
    price_dict: dict[str, dict[str, str | float | date | None]] = get_prices(symbol)

    share_dict: dict[str, float] = get_shares(symbol)
    
    cap_dict = {}
    
    for isodate, value_dict in price_dict.items():
        share_list = [ shares for qdate, shares in share_dict.items() if qdate <= isodate ]  # share_list will be empty if k (isodate) is too old
        
        target_shares: float | None = share_list[0] if share_list else None
        
        close: float | None = value_dict.get('close')
        
        if target_shares and close:   # filter out dates that do not have outstanding share number
            value_dict['shares'] = target_shares
            value_dict['cap'] = target_shares * close 
            cap_dict[isodate] = value_dict
            
    return cap_dict
        


async def main() -> None:
    
    x1, x2 = await asyncio.gather(
        async_listing_status(),
        async_shares_outstanding('AMD'),
    )

    
    pprint(x2)


if __name__ == '__main__':
    
    #asyncio.run(main())
    
    # x = get_closes_and_caps('AMD')
    # data = list(x.values())
    # pprint(data[:540], sort_dicts=False)
                       
    cap_dict: dict[str, dict[str, str | float | date | None]] = get_caps_shares('AMD')

    print(cap_dict)