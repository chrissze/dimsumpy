
# STANDARD LIBRARIES
from typing import Dict, List


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import pandas
from pandas.core.frame import DataFrame
import requests
from requests.models import Response


safari_headers: Dict[str, str] = {'User-Agent': 'Safari/13.1.1'}


def get_html_text(url: str) -> str :
    ''' 
    * INDEPENDENT *
    IMPORTS: requests
    '''
    html_response: Response = requests.get(url, headers=safari_headers)
    return html_response.text


def get_html_soup(url: str) -> BeautifulSoup :
    ''' 
    DEPENDS ON: get_html_text()
    IMPORTS: beautifulsoup4
    '''
    html_text: str = get_html_text(url)
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    return soup


def get_html_dataframes(url: str) -> List[DataFrame]:
    '''
    * INDEPENDENT *
    IMPORTS: beautifulsoup4, pandas, requests

    https://google.com   (has <table>)
    https://yahoo.com   (no <table>)
    https://googel.com   (INVALID SSL cert)

    If there is non <table> tag, soup_tables will be just be empty ResultRet [], soup.find_all() function is safe.
    
    I MUST ensure html_text has a <table> tag, otherwise pandas.read_html will have No tables found error.
    '''
    html_text: str = get_html_text(url)
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    soup_tables: ResultSet = soup.find_all('table')
    dataframes: List[DataFrame] = pandas.read_html(html_text, header=0) if soup_tables else []
    return dataframes


if __name__ == '__main__':

    s = input('which str to you want to input? ')

    x = get_html_dataframes(s) 
    print(x)


    