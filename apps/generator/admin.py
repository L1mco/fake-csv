from django.contrib import admin

# Register your models here.
from apps.generator.models import DataSet

admin.site.register(DataSet)