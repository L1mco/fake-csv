from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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

    @property
    def format_modified_date(self):
        return self.modified_date.strftime("%Y-%m-%d")


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
    range_from = models.IntegerField(
        blank=True, null=True, default=0, verbose_name='From'
    )
    range_to = models.IntegerField(
        blank=True, null=True, default=0, verbose_name='To'
    )
    order = models.IntegerField(verbose_name='Order')

    class Meta:
        verbose_name = 'Column'
        verbose_name_plural = 'Columns'

    def __str__(self):
        return f'{self.name} - {self.type}'

    def save(self, *args, **kwargs):
        if not self.type.is_range:
            self.range_from = None
            self.range_to = None

        super().save(*args, **kwargs)

    def clean(self):
        """
        Validate 'order', 'schema'  are unique together
        """
        order_not_unique_in_schema = (
            self.__class__.objects
            .filter(order=self.order, schema=self.schema)
            .exclude(id=self.id)
            .exists()
        )

        if order_not_unique_in_schema:
            raise ValidationError(
                'Selected order is not unique in this schema',
                code='unique_together',
            )


class ColumnType(models.Model):
    """ Model for column`s type """
    name = models.CharField(max_length=80, verbose_name='Name')
    is_range = models.BooleanField(default=False, verbose_name='Range?')

    class Meta:
        verbose_name = 'Column type'
        verbose_name_plural = 'Column types'

    def __str__(self):
        return f'{self.name}'
