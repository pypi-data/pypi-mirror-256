from datetime import datetime
from booyah.db.adapters.base_adapter import BaseAdapter

EQUAL_OPERATOR = '= ?'
LIKE_OPERATOR = 'like ?'
DIFFERENT_OPERATOR = '!= ?'
GREATER_THAN_OPERATOR = '> ?'
GREATER_THAN_OR_EQUAL_OPERATOR = '>= ?'
LESS_THAN_OPERATOR = '< ?'
LESS_THAN_OR_EQUAL_OPERATOR = '<= ?'
QUERY_OPERATORS = {
    'eq': EQUAL_OPERATOR,
    'like': LIKE_OPERATOR,
    'not_like': DIFFERENT_OPERATOR,
    'gt': GREATER_THAN_OPERATOR,
    'gte': GREATER_THAN_OR_EQUAL_OPERATOR,
    'lt': LESS_THAN_OPERATOR,
    'lte': LESS_THAN_OR_EQUAL_OPERATOR
}

class ModelQueryBuilder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.selected_attributes = []
        self.select_query = ''
        self.where_conditions = []
        self.joins = []
        self.order_by_attributes = []
        self.group_by_attributes = []
        self._limit = None
        self._offset = None
        self.scope = None
        self.db_adapter = BaseAdapter.get_instance()

    def all(self):
        self.select_all_columns()
        return self

    def find(self, id):
        self.select_all_columns()
        self.where(f"{self.model_class.table_name()}.id = {id}")
        return self

    def select_all_columns(self):
        columns = map(lambda column: f"{self.model_class.table_name()}.{column}", self.model_class.get_table_columns())
        self.select(", ".join(columns))
        self

    def select(self, *args):
        self.selected_attributes += args
        self.select_query = f"SELECT {','.join(self.selected_attributes)} FROM {self.model_class.table_name()}"
        return self

    def where(self, *args):
        if len(args) == 1:
            if isinstance(args[0], str):
                self.where_conditions.append(args[0])
            elif isinstance(args[0], list):
                if len(args[0]) == 1:
                    self.where_conditions.append(args[0][0])
                else:
                    result = args[0][0]
                    if len(args[0]) == 2 and isinstance(args[0][1], dict):
                        for k, v in args[0][1].items():
                            result = result.replace(f':{k}', self.sql_value(v))
                    else:
                        for i in range(1, len(args[0])):
                            result = self.replace_first_sql_value(result, self.sql_value(args[0][i]))
                    self.where_conditions.append(result)
            elif isinstance(args[0], dict):
                result = []
                for k, v in args[0].items():
                    if isinstance(v, list):
                        result.append(f'{k} IN ({self.sql_value(v)})')
                    else:
                        result.append(f'{k} = {self.sql_value(v)}')
                self.where_conditions.append(' AND '.join(result))
        else:
            if isinstance(args[1], list):
                condition = self.replace_first_sql_value(args[0], self.sql_value(args[1]))
            else:
                condition = f"{args[0]}"
                for operator in QUERY_OPERATORS.values():
                    if operator in condition:
                        condition = condition.replace(' ?', f" {self.sql_value(args[1])}")
                        self.where_conditions.append(condition)
                        return self
                    elif args[1] == None:
                        condition = f"{condition} is NULL"
                        self.where_conditions.append(condition)
                        return self
                operator = '' if ' ' in condition else " = "
                condition = f"{condition}{operator}{self.sql_value(args[1])}"
            self.where_conditions.append(condition)
        return self

    def replace_first_sql_value(self, sql, value):
        return sql.replace('?', value, 1)
    
    def sql_value(self, value):
        if isinstance(value, datetime):
            sql_escaped = value.isoformat()
            return f"\'{sql_escaped}\'"
        elif isinstance(value, str):
            sql_escaped = value.replace("'", "''")
            return f"\'{sql_escaped}\'"
        elif isinstance(value, list):
            return ','.join(str(self.sql_value(item)) for item in value)
        else:
            return value

    def exists(self, conditions):
        scope = self.select('1')
        for key, value in conditions.items():
            scope.where(key, value)
        return scope.count() > 0

    def offset(self, offset):
        self._offset = offset
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    def per_page(self, per_page):
        self._limit = per_page
        return self

    def page(self, page):
        self._offset = (page - 1) * self._limit
        return self

    def order(self, *args):
        self.order_by_attributes += args
        return self

    def group(self, *args):
        self.group_by_attributes += args
        return self

    def join(self, *args):
        join_clause = {
            'table': args[0],
            'on': args[1],
            'type': 'INNER'
        }
        if len(args) > 2:
            join_clause['type'] = args[2]
        join_clause = f"{join_clause['type']} JOIN {join_clause['table']} ON ({join_clause['on']}) "
        self.joins.append(join_clause)
        return self

    def left_join(self, *args):
        self.join(args[0], args[1], 'LEFT')
        return self

    def right_join(self, *args):
        self.join(args[0], args[1], 'RIGHT')
        return self

    def build_query(self):
        if self.select_query == '':
            self.select_all_columns()
        query = self.select_query

        if self.joins:
            query += ' ' + ' '.join(self.joins)
        if self.where_conditions:
            query += ' WHERE ' + ' AND '.join(self.where_conditions)
        if self.group_by_attributes:
            query += ' GROUP BY ' + ','.join(self.group_by_attributes)
        if self.order_by_attributes:
            query += ' ORDER BY ' + ','.join(self.order_by_attributes)
        if self._limit:
            query += f" LIMIT {self._limit}"
        if self._offset:
            query += f" OFFSET {self._offset}"
        return query.strip()
    
    def destroy_all(self):
        query = f"DELETE FROM {self.model_class.table_name()} WHERE " + ' AND '.join(self.where_conditions)
        self.db_adapter.execute(query, expect_result=False)

    def model_from_result(self, result):
        return self.model_class(dict(zip(self.model_class.get_table_columns(), result)))

    def raw_results(self):
        full_query = self.build_query()
        return self.db_adapter.fetch(full_query)

    def results(self):
        results = list(map(lambda result: self.model_from_result(result), self.raw_results()))
        self.cleanup()
        return results

    def count(self):
        full_query = self.build_query()
        full_query = f"SELECT COUNT(*) FROM ({full_query}) AS count"
        raw_results = self.db_adapter.fetch(full_query)
        self.cleanup()
        return raw_results[0][0]

    def first(self):
        self.limit = 1
        results = self.results()
        if results:
            return results[0]
        return None

    def last(self):
        results = self.results()
        if results:
            return results[len(results) - 1]
        return None

    def each(self, callback):
        for result in self.results():
            callback(result)

    def cleanup(self):
        self.select_query = ''
        self.selected_attributes = []
        self.where_conditions = []
        self.joins = []
        self.order_by_attributes = []
        self.group_by_attributes = []
        self._limit = None
        self._offset = None
        self.scope = None

    # Iteratable methods
    def __iter__(self):
        self.current_index = 0
        self._results = self.results()
        return self

    def __next__(self):
        try:
            result = self._results[self.current_index]
        except IndexError:
            raise StopIteration
        self.current_index += 1
        return result

    def __len__(self):
        return len(self.results())

    def __getitem__(self, key):
        return self.results()[key]

    def __setitem__(self, key, value):
        self.results()[key] = value

    def __delitem__(self, key):
        del self.results()[key]

    def __contains__(self, item):
        return item in self.results()

    def __reversed__(self):
        return reversed(self.results())