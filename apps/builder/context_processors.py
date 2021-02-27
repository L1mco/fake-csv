from apps.builder.constants import SEPARATORS, QUOTES


def common_data_context(request):
    context = {
        "SEPARATORS": list(separator[1] for separator in SEPARATORS),
        "QUOTES": list(quote[1] for quote in QUOTES)
    }

    return context
