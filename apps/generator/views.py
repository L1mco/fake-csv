from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.generator.models import Schema


class SchemaListView(LoginRequiredMixin, ListView):
    template_name = 'pages/schema_list.html'
    context_object_name = 'schemas'

    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user)
