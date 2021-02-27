from apps.generator.models import DataSet
from apps.services.base import BaseQueryService


class GeneratorService(BaseQueryService):
    """ Service Class for schema builder """
    model = DataSet

    @classmethod
    def create_dataset(cls, data):
        cls.model.objects.create(**data)
