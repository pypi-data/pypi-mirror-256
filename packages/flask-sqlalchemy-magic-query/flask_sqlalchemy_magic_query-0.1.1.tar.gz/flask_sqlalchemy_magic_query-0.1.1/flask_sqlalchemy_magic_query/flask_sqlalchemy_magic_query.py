from functools import wraps
from flask import request
from flask_sqlalchemy.model import Model
from sqlalchemy.orm import ColumnProperty, InstrumentedAttribute, RelationshipProperty, Query

from sqlalchemy.sql.elements import and_


def parse_magic_filter_key(
        model, filter_key: str, raise_errors: bool = False
):
    for attribute in filter_key.split("__"):
        column = getattr(model, attribute, None)
        if isinstance(column, InstrumentedAttribute):
            if isinstance(column.property, ColumnProperty):
                return model, attribute
            elif isinstance(column.property, RelationshipProperty):
                model = column.property.entity.class_
            else:
                if raise_errors:
                    raise AttributeError(f"Invalid filtering attribute: {filter_key}")
                return None
        else:
            if raise_errors:
                raise AttributeError(f"Invalid filtering attribute: {filter_key}")
            return None

    if raise_errors:
        raise AttributeError("No attribute found to filter on")
    return None


class Query(Query):
    def _get_base_model(self) -> Model:
        return self._raw_columns[0].entity_namespace

    def magic_filter(self, filters, raise_errors: bool = True):
        operations = []
        og_model = self._get_base_model()
        for key, value in filters.items():
            if parsed := parse_magic_filter_key(
                    og_model, key, raise_errors=raise_errors
            ):
                model, attribute_name = parsed

                operation = build_magic_filter_operation(
                    model, attribute_name, value, key.split("__")[1]
                )

                operations.append(operation)

        return operations


def build_magic_filter_operation(
        model, attribute_name: str, value: str, operator: str
):
    column = getattr(model, attribute_name)

    if operator == 'gte':
        return column >= value
    if operator == 'gt':
        return column > value
    if operator == 'lte':
        return column <= value
    if operator == 'lt':
        return column < value
    if operator == 'like':
        return column.like(value)
    if operator == 'in':
        return column.in_(value.split(','))

    return column == value


def filter_query(
        model
):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            query = Query(model)

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=1000, type=int)
            filtered_args = {i: request.args[i] for i in request.args if i != 'page' or i != 'per_page'}

            if filtered_args == {}:
                query_result = model.query.paginate(page=page, per_page=per_page, count=True)
            else:
                filters = query.magic_filter(filters=filtered_args)

                query_result = None

                for filter in filters:
                    query_result = model.query.filter(filter).paginate(
                        page=page, per_page=per_page, count=True)

            return func(data=query_result.items, total=query_result.total, *args, **kwargs)

        return decorated

    return wrapper
