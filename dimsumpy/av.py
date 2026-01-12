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
from pprint import pprint
import os





import httpx

from httpx import Response



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




def get_historical_options(symbol: str, isodate=None, datatype='json', apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    # https://www.alphavantage.co/documentation/#historical-options
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
    
    if isinstance(isodate, date):
        isodate = isodate.isoformat()
        params['date'] = isodate 
    
    if isinstance(isodate, datetime):
        isodate = isodate.date().isoformat()
        params['date'] = isodate 
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    data: dict[str, str | list[dict[str, str]]] = r.json()
    
    return data



# todo
def async_historical_options(symbol: str, isodate=None, datatype='json', apikey=None) -> dict[str, str | list[dict[str, str]]]:
    """
    # https://www.alphavantage.co/documentation/#historical-options
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
    
    if isinstance(isodate, date):
        isodate = isodate.isoformat()
        params['date'] = isodate 
    
    if isinstance(isodate, datetime):
        isodate = isodate.date().isoformat()
        params['date'] = isodate 
    
    r: Response = httpx.get('https://www.alphavantage.co/query', params=params)
    
    data: dict[str, str | list[dict[str, str]]] = r.json()
    
    return data




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
    x1, x2, x3, x4, x5 = await asyncio.gather(
        async_overview('AMD'),
        async_overview('NVDA'),
        async_overview('AAPL'),
        async_etf_profile('QQQ'),
        async_time_series_daily('META'),
    )

    print(x1, x2, x3, x4, x5)


if __name__ == '__main__':
    #asyncio.run(main())
    #pprint(get_overview('AMD'))
    pprint(get_historical_options('QQQ'))
    
    