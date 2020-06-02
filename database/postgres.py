from typing import List


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

##