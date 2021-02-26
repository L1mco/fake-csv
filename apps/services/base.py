import json
from abc import ABC

from django.template.loader import render_to_string


class BaseQueryService(ABC):

    @classmethod
    def parse_data(cls, data: bytes) -> dict:
        result = json.loads(data.decode())

        return result

    @staticmethod
    def get_html_template(request, tmp_name, data):
        return render_to_string(template_name=tmp_name,
                                context=data,
                                request=request)
