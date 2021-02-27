from django.forms import Form, CharField, TextInput, ChoiceField, Select

from apps.builder.constants import SEPARATORS, QUOTES


class SchemaCreateForm(Form):
    title = CharField(
        max_length=127,
        required=True,
        error_messages={'required': 'Must be title'},
        widget=TextInput(
            attrs={
                'placeholder': 'Title',
                'autocomplete': 'off',
                'id': 'schema_title',
                'class': 'form-control'
            }
        ),
    )
    separator = ChoiceField(
        choices=SEPARATORS,
        required=True,
        widget=Select(
            attrs={
                'autocomplete': 'off',
                'id': 'schema_separator',
                'class': 'form-control'
            }
        )
    )
    quote = ChoiceField(
        choices=QUOTES,
        required=True,
        widget=Select(
            attrs={
                'autocomplete': 'off',
                'id': 'schema_quote',
                'class': 'form-control'
            }
        )
    )
