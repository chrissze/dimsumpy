
# STANDARD LIBRARIES
from http.client import HTTPResponse
from io import StringIO
import shutil
from typing import Dict, List
import urllib

# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import pandas
from pandas.core.frame import DataFrame
import requests
from requests.models import Response


safari_headers: Dict[str, str] = {'User-Agent': 'Safari/13.1.1'}


def get_html_text(url: str) -> str :
    """ 
    * INDEPENDENT *
    IMPORTS: requests
    """
    html_response: Response = requests.get(url, headers=safari_headers)
    return html_response.text


def get_html_soup(url: str) -> BeautifulSoup :
    """ 
    DEPENDS ON: get_html_text()
    IMPORTS: beautifulsoup4
    """
    html_text: str = get_html_text(url)
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    return soup


def get_html_dataframes(url: str, header=None) -> List[DataFrame]:
    """
    * INDEPENDENT *
    IMPORTS: beautifulsoup4, pandas, requests

    https://google.com   (has <table>)
    https://yahoo.com   (no <table>)
    https://googel.com   (INVALID SSL cert)

    If there is non <table> tag, soup_tables will be just be empty ResultRet [], soup.find_all() function is safe.
    
    I MUST ensure html_text has a <table> tag, otherwise pandas.read_html will have No tables found error.

    for the header keyword argument, the default is None, that is no header row, if I want to have the first row as header row, I could write header=0) 
    """
    html_text: str = get_html_text(url)
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    soup_tables: ResultSet = soup.find_all('table')
    dataframes: List[DataFrame] = pandas.read_html(StringIO(html_text), header=header) if soup_tables else []
    return dataframes



def get_urllib_response(url: str) -> HTTPResponse :
    """ 
    * INDEPENDENT *
    IMPORTS: urllib
    """
    req = urllib.request.Request(url, headers=safari_headers)
    with urllib.request.urlopen(req) as response:
        return response
    

def get_urllib_text(url: str) -> str :
    """ 
    * INDEPENDENT *
    IMPORTS: urllib
    """
    req = urllib.request.Request(url, headers=safari_headers)
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8') 
    

def save_urllib_file(url: str, output: str='file.txt') -> None:
    """
    * INDEPENDENT *
    IMPORTS: shutil, urllib
    """
    req = urllib.request.Request(url, headers=safari_headers)
    with urllib.request.urlopen(req) as response, open(output, 'wb') as f:
        shutil.copyfileobj(response, f)
        
    

def get_csv_dataframe(url: str, header=None) -> DataFrame :
    """ 
    DEPENDS ON: get_urllib_text()
    IMPORTS: pandas, io
    """
    text: str = get_urllib_text(url)
    df = pandas.read_csv(StringIO(text), header=header)
    return df


if __name__ == '__main__':

    s = input('which str to you want to input? ')

    x = get_urllib_text(s) 
    print(x)


    
