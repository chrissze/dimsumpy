"""
I should put this into requirements.txt to install - psycopg[binary, pool]

psycopg Documentation:
https://www.psycopg.org/psycopg3/docs/

executemany:
    CORRECT:    cur.executemany(cmd, [('aa.com',),('bb.com',)])
    WRONG:    cur.executemany(cmd, ['aa.com', 'bb.com')

    executemany does not accept list() function as a sequence parameter        
    CORRECT: domain_list = list(my_generator) 
            cur.executemany(cmd, domain_list)
    WRONG: cur.executemany(cmd, list(my_generator))


"""

# STANDARD LIBS
from typing import Any, Dict, List, Tuple

# THIRD PARTY LIBS
import pandas
from pandas import DataFrame
from psycopg import Connection  # psycopg 3


def execute_psycopg(command: str, connection: Connection) -> None:
    """
    * INDEPENDENT *
    IMPORTS: psycopg

    the connection parameter can be a function that returns a psycopg 3 Connection. For example, make_psycopg_connection() in pizzapy program.

    con.commit() will just return None for successful execution.
    I can use pandas.read_sql if I want to fetch the result.
    """
    with connection as con:
        con.execute(command)
        con.commit()
    


def make_upsert_psycopg_query(table: str, columns: List[str], primary_key_list: List[str]) -> str:
    """
    * INDEPENDENT *

    make a psycopg version 3 Postgres UPSERT SQL string without semicolon.
    return SQL query example:
        INSERT INTO stock_guru (symbol, td, t, wealth_pc) VALUES (%s, %s, %s, %s) ON CONFLICT (symbol, td) DO UPDATE SET (t, wealth_pc) = (EXCLUDED.t, EXCLUDED.wealth_pc)
    """
    columns_str: str = ', '.join(columns)
    number_of_columns: int = len(columns)
    placeholders: str = ', '.join(['%s'] * number_of_columns)
    primary_key_str: str = ', '.join(primary_key_list)
    non_primary_key_columns: List[str] = [x for x in columns if x not in primary_key_list]
    non_primary_key_columns_str: str = ', '.join(non_primary_key_columns)
    update_part: str = ', '.join(list(map(lambda column: f'EXCLUDED.{column}', non_primary_key_columns)))
    query_str: str = f'INSERT INTO {table} ({columns_str}) VALUES ({placeholders}) ON CONFLICT ({primary_key_str}) DO UPDATE SET ({non_primary_key_columns_str}) = ({update_part})'
    return query_str



def upsert_psycopg(dict: Dict, table: str, primary_key_list: List[str], connection: Connection) -> str:
    """
    DEPENDS ON:  make_upsert_psycopg_query()
    IMPORTS: psycopg

    the connection parameter can be a function that returns a psycopg 3 Connection. For example, make_psycopg_connection() in pizzapy program.
    """
    query: str = make_upsert_psycopg_query(table, columns=dict.keys(), primary_key_list=primary_key_list)
    values = tuple(dict.values())
    with connection as con:
        con.execute(query, values)
        con.commit()
    query_and_values: str = f'{query} {values}'
    return query_and_values






def upsert_many_dataframe(dataframe: DataFrame, table: str, primary_key_list: List[str], connection: Connection) -> str:
    """
    DEPENDS ON:  make_upsert_psycopg_query()
    IMPORTS: psycopg, pandas

    df argument is a single dataframe with a header row.

    I have to convert it to tuples in order to be used in psycopg.

    the connection parameter can be a function that returns a psycopg 3 Connection. For example, make_psycopg_connection() in pizzapy program.

    this function is tested successfully on pizzapy/reference_example/executemany_success.py

    dataframe.values type is numpy.ndarray, it will not include the header row.
    entries' type is List of tuples
    """
    columns: List[str] = [] if dataframe.empty else dataframe.columns.tolist()
    entries = [] if dataframe.empty else [tuple(value) for value in dataframe.values]
    query: str = make_upsert_psycopg_query(table, columns=columns, primary_key_list=primary_key_list)    
    with connection as con:
        with con.cursor() as cur:
            cur.executemany(query, entries)
        con.commit()
    return query











def upsert_many_dicts(dictionaries: List[Dict], table: str, primary_key_list: List[str], connection: Connection) -> str:
    """
    DEPENDS ON:  make_upsert_psycopg_query()
    IMPORTS: psycopg

    dictionaries argument is a list of ProxyDict in pizzapy.

    dict.values() return a dict_values object, I have to convert it to tuple in order to be used in psycopg.

    the connection parameter can be a function that returns a psycopg 3 Connection. For example, make_psycopg_connection() in pizzapy program.

    this function is tested successfully on pizzapy/reference_example/executemany_success.py

    However, it is not practical to fetch mutiple DictProxies and accumulate them, then run this function. As this increase the code complexity and harder to debug. Not much time saved.

    I would rather loop through a list of stock symbols, fetch a DictProxy, and run upsert_psycopg() one by one.

    """
    columns: List[str] = dictionaries[0].keys() if dictionaries else []
    query: str = make_upsert_psycopg_query(table, columns=columns, primary_key_list=primary_key_list)
    values_list: List[Tuple] = [tuple(dict.values()) for dict in dictionaries]
    
    with connection as con:
        with con.cursor() as cur:
            cur.executemany(query, values_list)
        con.commit()
    return query



if __name__ == '__main__':
    q1 = make_upsert_psycopg_query('stock_guru', ['symbol', 'td', 't', 'wealth_pc'], ['symbol', 'td'])

    print('q1 is: ', q1)
    print()