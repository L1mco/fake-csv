from django.urls import path

from apps.builder.views import (
    SchemaListView, SchemaDetailView, SchemaInfoEditView, ColumnCreateView,
    SchemaCreateView, ColumnUpdateView
)

app_name = 'builder'

urlpatterns = [
    path('', SchemaListView.as_view(), name='schema_list'),
    path('schema/<int:pk>/', SchemaDetailView.as_view(), name='schema_detail'),
    path('schema/create/', SchemaCreateView.as_view(), name='schema_create'),
    path('schemas/main/', SchemaInfoEditView.as_view(), name='schema_main_edit'),
    path('column/create/', ColumnCreateView.as_view(), name='column_create'),
    path('column/update/', ColumnUpdateView.as_view(), name='column_update'),
]
