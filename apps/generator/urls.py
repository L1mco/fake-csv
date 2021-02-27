from django.urls import path

from apps.generator.views import (
    DataSetListView
)

app_name = 'generator'

urlpatterns = [
    path('', DataSetListView.as_view(), name='dataset_list'),
]
