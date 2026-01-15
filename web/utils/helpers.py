from datetime import datetime
from typing import Any
from django.contrib import messages
from django.http import HttpRequest


MONTH_NAMES_MAPPING = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
}


def format_api_date(original_date_str, original_format, desired_format):
    date_obj = datetime.strptime(original_date_str, original_format)
    return date_obj.strftime(desired_format)


def show_error_message(request: HttpRequest, response: Any, extra_message: str) -> None:
    """
    Exibe uma mensagem de erro no template com base em uma resposta da API.
    """
    error = response.json().get("detail", response.status_code)
    messages.error(request, f"{extra_message}: {error}", extra_tags="danger")


def show_success_message(request: HttpRequest, extra_message: str) -> None:
    """
    Exibe uma mensagem de sucesso genérica.
    """
    messages.success(request, extra_message)
