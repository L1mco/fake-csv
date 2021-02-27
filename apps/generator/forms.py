from django.forms import ModelChoiceField, IntegerField, TextInput, Form, Select

from apps.builder.models import Schema


class DataSetForm(Form):
    rows = IntegerField(
        required=True,
        max_value=1000000,
        widget=TextInput(
            attrs={
                'placeholder': 'Rows',
                'autocomplete': 'off',
                'id': 'rows',
                'class': 'form-control',
                'type': 'number',
                'max': '100000',
                'min': '1'
            }
        ),
    )

    schema = ModelChoiceField(
        queryset=Schema.objects.all(),
        required=True,
        widget=Select(
            attrs={
                'autocomplete': 'off',
                'id': 'schema',
                'class': 'form-control'
            }
        )
    )
