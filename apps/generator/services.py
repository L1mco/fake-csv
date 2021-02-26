from django.db import DataError
from django.db.models import Prefetch

from apps.generator.models import Schema, Column, ColumnType
from apps.services.base import BaseQueryService


class GeneratorService(BaseQueryService):
    """ Service Class for schema generator """
    schema_model = Schema
    column_model = Column

    @classmethod
    def update_schema_info(cls, data, schema_id):
        try:
            return cls.schema_model.objects.filter(id=schema_id).update(**data)
        except DataError:
            return None

    @classmethod
    def get_schema_by_id(cls, schema_id):
        return cls.schema_model.objects.filter(id=schema_id).first()

    @classmethod
    def get_column_type_by_name(cls, type_name):
        return ColumnType.objects.filter(name=type_name).first()

    @classmethod
    def create_schema_column(cls, data):
        schema = cls.get_schema_by_id(data.pop('schema_id'))
        column_type = cls.get_column_type_by_name(data.pop('type_name'))
        columns = (
            cls.column_model.objects
                .filter(schema=schema, order=data.get('order'))
        )
        if columns.exists():
            return None

        return cls.column_model.objects.create(schema=schema, type=column_type, **data)

    @classmethod
    def delete_schema(cls, schema_id):
        schema = cls.get_schema_by_id(schema_id)
        if schema:
            return schema.delete()
        return None

    @classmethod
    def get_column_by_id(cls, column_id):
        return cls.column_model.objects.filter(id=column_id).first()

    @classmethod
    def check_column_order(cls, column, order):
        return (
            cls.column_model.objects
                .filter(order=order, schema=column.schema)
                .exclude(id=column.id)
                .exists()
        )

    @classmethod
    def update_column(cls, data):
        column = cls.get_column_by_id(data.pop('column_id'))
        column_info = data['column_info']

        if not column:
            return None

        update_column_value = column_info['value']
        update_column_field = column_info['field']

        if update_column_field == 'type':
            column_type = cls.get_column_type_by_name(update_column_value)
            column.type = column_type
        elif update_column_field == 'name':
            column.name = update_column_value
        elif update_column_field == 'range_from':
            column.range_from = update_column_value
        elif update_column_field == 'range_to':
            column.range_to = update_column_value
        elif update_column_field == 'order':
            if cls.check_column_order(column, update_column_value):
                return None
            column.order = update_column_value

        column.save(update_fields=[update_column_field])

        return column

    @classmethod
    def delete_column(cls, column_id):
        column = cls.get_column_by_id(column_id)
        if column:
            return column.delete()
        return None
