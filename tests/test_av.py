
import pytest

from dimsumpy.av import  get_balance_sheet, async_balance_sheet, get_etf_profile, async_etf_profile

from dimsumpy.av import  get_balance_sheet, get_cap, async_cap, get_cap_aum, get_close, async_close, get_etf_aum, async_etf_aum, get_etf_list, async_etf_list


######################
### TEST ENDPOINTS ###
######################


def test_get_balance_sheet() -> None:
    
    data: dict[str, str | list[dict[str, str]]] = get_balance_sheet('AMD')
    s = data.get('symbol')
    
    assert isinstance(s, str)
    assert s == 'AMD'
    

@pytest.mark.asyncio
async def test_async_balance_sheet() -> None:
    
    data: dict[str, str | list[dict[str, str]]] = await async_balance_sheet('AMD')
    s = data.get('symbol')
    
    assert isinstance(s, str)
    assert s == 'AMD'
    



def test_get_etf_profile() -> None:
    
    data: dict[str, str | list[dict[str, str]]] = get_etf_profile('QQQ')
    aum = data.get('net_assets')
    
    assert isinstance(aum, str)
    assert float(aum) > 100_000_000_000
    
    


@pytest.mark.asyncio
async def test_async_etf_profile() -> None:
    """
    
    """
    data: dict[str, str | list[dict[str, str]]] = await async_etf_profile('QQQ')
    aum = data.get('net_assets')
    
    assert isinstance(aum, str)
    assert float(aum) > 100_000_000_000
    
    
    
    
    
    
    
############################
### TEST STOCK FUNCTIONS ###
############################


def test_get_cap() -> None:
    c1 = get_cap('AMD')
    c2 = get_cap('QQQ')
    c3 = get_cap('XXXXXX')
    
    assert isinstance(c1, float)
    assert c1 > 100_000_000_000.0
    
    assert c2 is None
    assert c3 is None
    

@pytest.mark.asyncio
async def test_async_cap():
    c1 = await async_cap('NVDA')
    c2 = await async_cap('SPY')
    c3 = await async_cap('XXXXXX')
    
    assert isinstance(c1, float)
    assert c1 > 4_000_000_000_000.0

    assert c2 is None
    assert c3 is None



def test_get_cap_aum() -> None:
    c1 = get_cap_aum('AMD')
    c2 = get_cap_aum('QQQ')
    c3 = get_cap('XXXXXX')
    
    assert isinstance(c1, float)
    assert c1 > 100_000_000_000.0
    
    assert isinstance(c2, float)
    assert c2 > 100_000_000_000.0
    
    assert c3 is None



def test_get_close() -> None:
    c1 = get_close('AMD')
    c2 = get_close('QQQ')
    c3 = get_close('XXXXXX')
    
    assert isinstance(c1, float)
    assert c1 > 100.0
    assert isinstance(c2, float)
    assert c2 > 300.0
    assert c3 is None
    

@pytest.mark.asyncio
async def test_async_close():
    c1 = await async_close('NVDA')
    c2 = await async_close('SPY')
    c3 = await async_close('XXXXXX')
    
    assert isinstance(c1, float)
    assert c1 > 100.0
    assert isinstance(c2, float)
    assert c2 > 300.0
    assert c3 is None
    

def test_get_etf_aum() -> None:
    c1 = get_etf_aum('AMD')
    c2 = get_etf_aum('QQQ')
    c3 = get_cap('XXXXXX')
    
    assert c1 is None
    
    assert isinstance(c2, float)
    assert c2 > 100_000_000_000.0
    
    assert c3 is None



@pytest.mark.asyncio
async def test_async_etf_aum():
    c1 = await async_etf_aum('NVDA')
    c2 = await async_etf_aum('SPY')
    c3 = await async_etf_aum('XXXXXX')
    
    assert c1 is None
    
    assert isinstance(c2, float)
    assert c2 > 100_000_000_000.0
    
    assert c3 is None



def test_get_etf_list() -> None:
    xs = get_etf_list()

    assert isinstance(xs, list)
    assert len(xs) > 3000
    assert 'QQQ' in xs
    
    

@pytest.mark.asyncio
async def test_async_etf_list():
    xs = await async_etf_list()

    assert isinstance(xs, list)
    assert len(xs) > 3000
    assert 'SPY' in xs
    
    