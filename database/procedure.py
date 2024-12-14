from database.DBcm import DBContextManager
from pymysql.err import Error


def call_proc(db_config: dict, proc_name: str, params: tuple) -> object:
    res = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not created')
        try:
            res = cursor.callproc(proc_name, params)
        except Error as err:
            print("error in procedure.py:",err)
    return res


def call_proc_state(db_config: dict, proc_name: str, params: tuple):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not created')
        try:
            cursor.callproc(proc_name, params)
        except Error as err:
            return err
    return None
