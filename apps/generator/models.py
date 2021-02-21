from django.contrib.auth.models import User
from django.db import models

from apps.generator.constants import SEPARATORS, QUOTES


class Schema(models.Model):
    """ Model for csv schema """
    owner = models.ForeignKey(
        User, related_name='schemas', on_delete=models.CASCADE,
        verbose_name='Owner'
    )
    title = models.CharField(max_length=127, verbose_name='Title')
    modified_date = models.DateField(auto_now=True)
    separator = models.CharField(
        max_length=50, choices=SEPARATORS, default='COMMA',
        verbose_name='separator type'
    )
    quote = models.CharField(
        max_length=50, choices=QUOTES, default='QUOTE',
        verbose_name='Quote type'
    )

    class Meta:
        verbose_name = 'Schema'
        verbose_name_plural = 'Schemas'

    def __str__(self):
        return f'{self.title}'


class Column(models.Model):
    """ Model for schema`s column """
    schema = models.ForeignKey(
        Schema, on_delete=models.CASCADE, related_name='columns',
        verbose_name='Schema'
    )
    name = models.CharField(max_length=127, verbose_name='Name')
    type = models.ForeignKey(
        'ColumnType', on_delete=models.PROTECT, verbose_name='Type'
    )
    order = models.IntegerField(verbose_name='Order')

    class Meta:
        verbose_name = 'Column'
        verbose_name_plural = 'Columns'

    def __str__(self):
        return f'{self.name} - {self.type}'


class ColumnType(models.Model):
    """ Model for column`s type """
    name = models.CharField(max_length=80, verbose_name='Name')
    range_from = models.IntegerField(blank=True, null=True, verbose_name='From')
    range_to = models.IntegerField(blank=True, null=True, verbose_name='From')

    class Meta:
        verbose_name = 'Column type'
        verbose_name_plural = 'Column types'

    def __str__(self):
        return f'{self.name}'
