'''

DOCS:
    https://www.alphavantage.co/documentation/


    
NOTES:

- my USD 50 plan is 5 limited at 5 requests per second

- httpx.AsyncClient()'s default timeout is 5 seconds.


async def main() -> None:
    x1 = await gets_overview('AMD')
    x2 = await gets_overview('NVDA')
    x3 = await gets_overview('AAPL')
    x4 = await gets_overview('META')
    x5 = await gets_overview('GOOGL')

    print(x1)
    print(x2)
    print(x3)
    print(x4)
    print(x5)

'''

import asyncio

from datetime import date, datetime
from io import StringIO

from pprint import pprint
import os





import httpx

from httpx import Response

import pandas as pd




def get_etf_profile(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:

    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {'function': 'ETF_PROFILE', 'symbol': symbol, 'apikey': apikey}
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    r.raise_for_status()
    
    data: dict[str, str | list[dict[str, str]]] = r.json()
    
    return data



async def async_etf_profile(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:
    if apikey is None:
        apikey = os.getenv("AV_API_KEY")

    params: dict[str, str] = {'function': 'ETF_PROFILE', 'symbol': symbol, 'apikey': apikey}

    async with httpx.AsyncClient() as client:
        r = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, str | list[dict[str, str]]] = r.json()

    return data






def get_etf_aum(symbol: str) -> float | None:

    data: dict[str, str | list[dict[str, str]]] = get_etf_profile(symbol)

    aum_str: str | None = data.get('net_assets')

    aum: float | None = float(aum_str) if aum_str else None

    return aum



async def async_etf_aum(symbol: str) -> float | None:

    data: dict[str, str | list[dict[str, str]]] = await async_etf_profile(symbol)

    aum_str: str | None = data.get('net_assets')

    aum: float | None = float(aum_str) if aum_str else None

    return aum







def get_historical_options(symbol: str, isodate=None, datatype='json', apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
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




def get_overview(symbol: str, apikey=None) -> dict[str, str]:

    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': apikey}
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)

    r.raise_for_status()
    
    data: dict[str, str] = r.json()
    
    return data



async def async_overview(symbol: str, apikey=None) -> dict[str, str]:
    if apikey is None:
        apikey = os.getenv("AV_API_KEY")

    params: dict[str, str] = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': apikey}

    async with httpx.AsyncClient() as client:
        r: Response = await client.get('https://www.alphavantage.co/query', params=params)
        r.raise_for_status()
        data: dict[str, str] = r.json()

    return data








def get_time_series_daily(symbol: str, outputsize='compact', datatype='json', apikey=None) -> dict[str, dict[str, str] | dict[str, dict[str, str]]]:

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
    x1, x2 = await asyncio.gather(
        async_overview('AMD'),
        async_listing_status(),
    )

    print(x1, x2)


if __name__ == '__main__':
    asyncio.run(main())
    #pprint(get_overview('AMD'))
    #pprint(get_listing_status(state='delisted'))
    
    