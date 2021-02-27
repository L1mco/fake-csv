from django.contrib import admin

from apps.builder.models import ColumnType, Column, Schema

admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(ColumnType)
