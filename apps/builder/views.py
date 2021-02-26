from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, View, FormView

from apps.builder.forms import SchemaCreateForm
from apps.builder.models import Schema, Column, ColumnType
from apps.services.fabric import ServiceClasses


class AbstractLoginRequiredView(LoginRequiredMixin, View):
    services = ServiceClasses


class SchemaListView(AbstractLoginRequiredView, ListView):
    template_name = 'pages/schema_list.html'
    context_object_name = 'schemas'

    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        data = self.services.builder.parse_data(data=request.body)
        if self.services.builder.delete_schema(data['schema_id']):
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'success': False}, status=400)


class SchemaDetailView(AbstractLoginRequiredView):
    template_name = 'pages/schema_detail.html'

    def get(self, request, *args, **kwargs):
        context = {
            'schema': (
                Schema.objects
                .filter(owner=request.user, id=kwargs['pk'])
                .prefetch_related(
                    Prefetch(
                        lookup='columns',
                        queryset=(
                            Column.objects.order_by('order')
                        )
                    )
                )
                .first()
            ),
            'column_types': ColumnType.objects.all()
        }

        return render(request, self.template_name, context)


class SchemaInfoEditView(AbstractLoginRequiredView):
    template_name = 'pages/schema_detail.html'

    def post(self, request, *args, **kwargs):
        data = self.services.builder.parse_data(data=request.body)
        schema_id = data.pop('schema_id')
        schema = self.services.builder.update_schema_info(data, schema_id)
        if schema:
            return JsonResponse({'success': True}, status=200)

        return JsonResponse({'success': False}, status=400)


class SchemaCreateView(AbstractLoginRequiredView, FormView):
    template_name = 'pages/schema_create.html'
    form_class = SchemaCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['column_types'] = ColumnType.objects.all()
        return context

    def form_valid(self, form):
        schema = (
            Schema.objects.create(owner=self.request.user, **form.cleaned_data)
        )

        return redirect(reverse('builder:schema_detail', args=(schema.pk,)))


class ColumnCreateView(AbstractLoginRequiredView):
    template_name = 'components/existed_columns.html'

    def post(self, request, *args, **kwargs):
        data = self.services.builder.parse_data(data=request.body)
        column = self.services.builder.create_schema_column(data)

        if not column:
            return JsonResponse({'success': False}, status=400)

        context = {
            'column': column,
            'column_types': ColumnType.objects.all()
        }
        html = render_to_string(
            template_name=self.template_name,
            context=context, request=self.request,
        )

        return JsonResponse({'rendered_html': html}, status=200)


class ColumnUpdateView(AbstractLoginRequiredView):
    def patch(self, request, *args, **kwargs):
        data = self.services.builder.parse_data(data=request.body)
        if self.services.builder.update_column(data):
            return JsonResponse({'success': True}, status=200)

        return JsonResponse({'success': False}, status=400)

    def delete(self, request, *args, **kwargs):
        data = self.services.builder.parse_data(data=request.body)
        if self.services.builder.delete_column(data['column_id']):
            return JsonResponse({'success': True}, status=200)

        return JsonResponse({'success': False}, status=400)
