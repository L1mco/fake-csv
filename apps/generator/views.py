from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.builder.models import Schema
from apps.builder.views import AbstractLoginRequiredView
from apps.generator.forms import DataSetForm
from apps.generator.models import DataSet


class DataSetListView(AbstractLoginRequiredView, FormView):
    template_name = 'pages/dataset_list.html'
    form_class = DataSetForm
    success_url = reverse_lazy('generator:dataset_list')

    def get_context_data(self, **kwargs):
        context = super(DataSetListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['datasets'] = (
            DataSet.objects
            .select_related('schema__owner')
            .filter(schema__owner=user)
            .order_by('-created_date')
        )
        context['schemas'] = (
            Schema.objects.filter(owner=user)
        )
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['schema'].queryset = (
            Schema.objects.filter(owner=self.request.user)
        )

        return form

    def form_valid(self, form):
        self.services.generator.create_dataset(form.cleaned_data)
        return super(DataSetListView, self).form_valid(form)
