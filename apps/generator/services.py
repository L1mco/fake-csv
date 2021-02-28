from apps.generator.models import DataSet
from apps.services.base import BaseQueryService


class GeneratorService(BaseQueryService):
    """ Service Class for schema builder """
    model = DataSet

    @classmethod
    def create_dataset(cls, data):
        return cls.model.objects.create(**data)

    @classmethod
    def get_dataset_by_id(cls, dataset_id):
        return cls.model.objects.filter(id=dataset_id).first()

    @classmethod
    def get_dataset_headers(cls, dataset):
        schema = dataset.schema
        columns = schema.columns.order_by('order')

        return list(column.name for column in columns)

    @classmethod
    def get_column_types(cls, dataset):
        schema = dataset.schema
        columns = schema.columns.order_by('order')
        types = []
        for column in columns:
            types.append({
                'name': column.type.name,
                'from': column.range_from,
                'to': column.range_to,
            })

        return types

    @classmethod
    def get_user_datasets(cls, user):
        return (
            DataSet.objects
            .select_related('schema__owner')
            .filter(schema__owner=user)
        )

    @classmethod
    def check_dataset_is_ready(cls, dataset):
        return dataset.id if dataset.ready else None
