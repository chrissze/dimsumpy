from typing import Any, Dict, List

from pandas import DataFrame
from psycopg2.extensions import connection, cursor

def make_psycopg_upsert_query(table_name: str, columns: List[str], primary_key_list: List[str]) -> str:
    '''
    * INDEPENDENT *

    make a psycopg version 3 Postgres UPSERT SQL string without semicolon.
    return SQL query example:
        INSERT INTO stock_guru (symbol, td, t, wealth_pc) VALUES (%s, %s, %s, %s) ON CONFLICT (symbol, td) DO UPDATE SET (t, wealth_pc) = (EXCLUDED.t, EXCLUDED.wealth_pc)
    '''
    columns_str: str = ', '.join(columns)
    number_of_columns: int = len(columns)
    placeholders: str = ', '.join(['%s'] * number_of_columns)
    primary_key_str: str = ', '.join(primary_key_list)
    non_primary_key_columns: List[str] = [x for x in columns if x not in primary_key_list]
    non_primary_key_columns_str: str = ', '.join(non_primary_key_columns)
    update_part: str = ', '.join(list(map(lambda column: f'EXCLUDED.{column}', non_primary_key_columns)))
    query_str: str = f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders}) ON CONFLICT ({primary_key_str}) DO UPDATE SET ({non_primary_key_columns_str}) = ({update_part})'
    return query_str




def psycopg_upsert(dict: Dict, table: str, primary_key_list: List[str], con: connection) -> str:
    '''
    Get the first value(symbol) of the primary_key_list by
        symbol: Any = dict.get(primary_key_list[0])
    
    I should place symbol as first element of keys, so that it can be returned
    '''
    try:
        c: cursor = con.cursor()
        query: str = make_psycopg_upsert_query(table, dict.keys(), primary_key_list)
        values = tuple(dict.values())
        print(f'query is {query}')
        c.execute(query, values)
        c.close()
        con.commit()
        pkvalue: Any = dict.get(primary_key_list[0])
        return str(pkvalue) # s
    except Exception as err:
        print(err)
        return str(err)



def execute_postgres_command(command: str, con: connection ) -> str:
    '''
    There might be similar function in the official psycopg
    '''
    try:
        c: cursor = con.cursor()
        c.execute(command)
        c.close()
        result = con.commit()
        return str(result)
    except Exception as err:
        print(err)
        return str(err)

if __name__ == '__main__':
    q1 = make_psycopg_upsert('stock_guru', ['symbol', 'td', 't', 'wealth_pc'], ['symbol', 'td'])

    print('q1 is: ', q1)
    print()