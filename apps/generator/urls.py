from django.urls import path

from apps.generator.views import SchemaListView

app_name = 'generator'

urlpatterns = [
    path('schemas/', SchemaListView.as_view(), name='schema_list'),
]
