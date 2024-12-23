from dataclasses import dataclass
from database.select import select_list
from database.procedure import call_proc_state
import json
from pathlib import Path

@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool


def generate_name(name: str):
    current_dir = Path(__file__).resolve().parent
    neighbor_dir = current_dir.parent / 'data'
    with open(neighbor_dir/"names.json", 'r', encoding='utf-8') as f:
        query_names = json.load(f)
    return query_names[name]


def generate_menu_list(user_role: str, menu: str):
    current_dir = Path(__file__).resolve().parent
    neighbor_dir = current_dir.parent / 'data'
    with open(neighbor_dir/'query.json', 'r', encoding='utf-8') as f:
        query_file = json.load(f)
    with open(neighbor_dir/"names.json", 'r', encoding='utf-8') as f:
        query_names = json.load(f)
    result = list()
    for item in query_file[user_role][menu]:
        result.append([item, query_names[item]])
    return result


def generate_header(sqlheader : list):
    current_dir = Path(__file__).resolve().parent
    neighbor_dir = current_dir.parent / 'data'
    with open(neighbor_dir/"table_namespace.json", 'r', encoding='utf-8') as f:
        query_file = json.load(f)
    res = list()
    for item in sqlheader:
        res.append(query_file[item])
    return res


def show_resource(db_config, sql_provider, resource_name):
    _sql = sql_provider.get('table.sql', tablename=resource_name)
    name = generate_name(resource_name)
    result, schema = select_list(db_config, _sql)
    if result or schema:
        return ProductInfoRespronse((name, generate_header(schema), result), error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Ошибка при получении данных.", status=False)


def create_report(db_config, proc_name, user_data):
    year = (user_data.get('report_date')).split("-")[0]
    month = (user_data.get('report_date')).split("-")[1]
    err = call_proc_state(db_config, proc_name, (year, month))
    if not err:
        return ProductInfoRespronse((), error_message="", status=True)
    else:
        return ProductInfoRespronse((), error_message=err.args[1], status=False)



