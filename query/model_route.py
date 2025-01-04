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


def generate_filtermenu(tablename, db_config):
    current_dir = Path(__file__).resolve().parent
    neighbor_dir = current_dir.parent / 'data'
    with open(neighbor_dir/'filtermenu.json', 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    with open(neighbor_dir/"table_namespace.json", 'r', encoding='utf-8') as f:
        query_file = json.load(f)
    tmp = tmp[tablename]
    for i in tmp:
        i['local'] = query_file[i['name']]
        if i['type'] == 'select' and 'values' not in i:
            _sql = i['sql']
            result, schema = select_list(db_config, _sql)
            i['values'] = [i[0] for i in result]
    return tmp


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


def generate_where_clause(form_data):
    where_clauses = []
    # Словарь для хранения пар 'начало' и 'конец' диапазона
    date_ranges = {}

    for field, value in form_data.items():
        # Обработка поля month_year
        if field == 'month_year' and value:
            try:
                # Пытаемся разделить значение на месяц и год
                year, month = value.split('-')
                where_clauses.append(f"`month` = {month} AND `year` = {year}")
            except ValueError:
                # Если значение не соответствует формату YYYY-MM, можем игнорировать или вызвать ошибку
                pass
        # Обработка дат (_begin, _end)
        elif field.endswith('_begin') or field.endswith('_end'):
            base_field = field.rsplit('_', 1)[0]
            if base_field not in date_ranges:
                date_ranges[base_field] = {'begin': None, 'end': None}

            if field.endswith('_begin'):
                date_ranges[base_field]['begin'] = value
            elif field.endswith('_end'):
                date_ranges[base_field]['end'] = value
        else:
            # Обработка обычных полей для точного поиска
            where_clauses.append(f"{field} = '{value}'")

    # Обрабатываем диапазоны дат
    for field, range_values in date_ranges.items():
        begin = range_values['begin']
        end = range_values['end']

        if begin and end:
            where_clauses.append(f"{field} BETWEEN '{begin}' AND '{end}'")
        elif begin:
            where_clauses.append(f"{field} >= '{begin}'")
        elif end:
            where_clauses.append(f"{field} <= '{end}'")

    # Если есть условия, соединяем их через 'AND'
    if where_clauses:
        return "WHERE " + " AND ".join(where_clauses)
    else:
        return ""


def show_resource(db_config, sql_provider, resource_name, filterdata=None):
    with open(Path(__file__).parent/"sql"/"tables.json") as f:
        sql_file = json.load(f)
    _sql = sql_file[resource_name]
    name = generate_name(resource_name)
    filtermenu = generate_filtermenu(resource_name, db_config)
    if filterdata:
        _sql = sql_provider.get('filter.sql', query=_sql[:-1], detail=generate_where_clause(filterdata))
    result, schema = select_list(db_config, _sql)
    if result or schema:
        return ProductInfoRespronse((name, generate_header(schema), result, filtermenu), error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Ошибка при получении данных.", status=False)


def create_report(db_config, proc_name, user_data):
    year = (user_data.get('report_date')).split("-")[0]
    month = (user_data.get('report_date')).split("-")[1]
    err = call_proc_state(db_config, proc_name, (year, month))
    if not err:
        return ProductInfoRespronse((), error_message="", status=True)
    else:
        return ProductInfoRespronse((), error_message=err.args[1], status=False)


