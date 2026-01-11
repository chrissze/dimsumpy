'''

DOCS:
    https://www.alphavantage.co/documentation/


    
NOTES:
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

from pprint import pprint
import os





import httpx




def get_overview(symbol: str, apikey=None) -> dict[str, str]:

    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': apikey}
    
    data: dict[str, str] = httpx.get('https://www.alphavantage.co/query', params=params).json()
    
    return data



async def gets_overview(symbol: str, apikey=None) -> dict[str, str]:
    if apikey is None:
        apikey = os.getenv("AV_API_KEY")

    params: dict[str, str] = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': apikey}

    async with httpx.AsyncClient() as client:
        resp = await client.get('https://www.alphavantage.co/query', params=params)
        resp.raise_for_status()
        data: dict[str, str] = resp.json()

    return data







def get_etf_profile(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:

    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {'function': 'ETF_PROFILE', 'symbol': symbol, 'apikey': apikey}
    
    data: dict[str, str | list[dict[str, str]]] = httpx.get('https://www.alphavantage.co/query', params=params).json()
    
    return data



async def gets_etf_profile(symbol: str, apikey=None) -> dict[str, str | list[dict[str, str]]]:
    if apikey is None:
        apikey = os.getenv("AV_API_KEY")

    params: dict[str, str] = {'function': 'ETF_PROFILE', 'symbol': symbol, 'apikey': apikey}

    async with httpx.AsyncClient() as client:
        resp = await client.get('https://www.alphavantage.co/query', params=params)
        resp.raise_for_status()
        data: dict[str, str | list[dict[str, str]]] = resp.json()

    return data




def get_time_series_daily(symbol: str, apikey=None, outputsize='compact', datatype='json') -> dict[str, dict[str, str] | dict[str, dict[str, dict]]]:

    if apikey is None:
        apikey = os.getenv('AV_API_KEY')
        
    params: dict[str, str] = {
        'function': 'TIME_SERIES_DAILY', 
        'symbol': symbol, 
        'apikey': apikey,
        'outputsize': outputsize,
        'datatype': datatype,
        }
    
    data: dict[str, str] = httpx.get('https://www.alphavantage.co/query', params=params).json()
    
    return data


async def main() -> None:
    x1, x2, x3, x4, x5 = await asyncio.gather(
        gets_overview('AMD'),
        gets_overview('NVDA'),
        gets_overview('AAPL'),
        gets_overview('META'),
        gets_etf_profile('QQQ'),
    )

    print(x1, x2, x3, x4, x5)


if __name__ == '__main__':
    #asyncio.run(main())
    pprint(get_time_series_daily('AMD'))
    
    