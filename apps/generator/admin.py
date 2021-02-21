from django.contrib import admin

from apps.generator.models import ColumnType, Column, Schema

admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(ColumnType)
