from typing import Any, Dict, List
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
    c: cursor = con.cursor()
    query: str = upsertquery(table, dict.keys(), primarykeys)
    values = tuple(dict.values())
    c.execute(query, values)
    c.close()
    con.commit()
    pkvalue: Any = dict.get(primarykeys[0])
    return str(pkvalue)


