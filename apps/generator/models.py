from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.builder.models import Schema
from utils.upload_dataset import upload_instance


class DataSet(models.Model):
    schema = models.ForeignKey(
        Schema, related_name='datasets', on_delete=models.CASCADE,
        verbose_name='Schema'
    )
    rows = models.PositiveIntegerField(verbose_name='Rows')
    created_date = models.DateField(auto_now_add=True)
    ready = models.BooleanField(default=False, verbose_name='Ready')
    file = models.FileField(
        upload_to=upload_instance, blank=True, null=True, verbose_name='File'
    )

    class Meta:
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'

    def __str__(self):
        return f'{self.schema.title} - {self.created_date.strftime("%Y-%m-%d")}'

    @property
    def format_created_date(self):
        return self.created_date.strftime("%Y-%m-%d")


@receiver(post_save, sender=DataSet)
def generate_trigger(instance, created, **kwargs):
    from apps.generator.tasks import generate_dataset_data
    if created:
        generate_dataset_data.delay(instance.id)
