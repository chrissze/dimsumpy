from typing import Any, Dict, List

from pandas import DataFrame
from psycopg2.extensions import connection, cursor

def upsertquery(tablename: str, cols: List[str], keys: List[str]) -> str:
    cols_str = ', '.join(cols)
    l = len(cols)
    marks = ', '.join(['%s'] * l)
    keys_str = ', '.join(keys)
    cols_nonkey = [x for x in cols if x not in keys]
    cols_nonkey_str = ', '.join(cols_nonkey)
    update_str = ', '.join(list(map(lambda s: 'EXCLUDED.' + s, cols_nonkey)))
    query_str = ''.join(['INSERT INTO ', tablename, ' (', cols_str, ') VALUES (', marks
                        , ') ON CONFLICT (', keys_str, ') DO UPDATE SET (', cols_nonkey_str
                        , ') = (', update_str, ')'])
    return query_str


def upsert_dict(table: str, dict: Dict, primarykeys: List[str], con: connection) -> str:
    """ I should place symbol as first element of keys, so that it can be returned"""
    try:
        c: cursor = con.cursor()
        query: str = upsertquery(table, dict.keys(), primarykeys)
        values = tuple(dict.values())
        print(f'query is {query}')
        c.execute(query, values)
        c.close()
        con.commit()
        pkvalue: Any = dict.get(primarykeys[0])
        return str(pkvalue) # should be the symbol
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

