from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from src.client.finance import FinanceAPIClient
from utils.decorators import validate_session
from datetime import datetime
from utils.helpers import format_api_date
from icecream import ic


@validate_session
def expenses_list(request, context):
    return render(
        request=request, template_name="finance_expenses_list.html", context=context
    )


@validate_session
def revenues_list(request, context):
    return render(
        request=request, template_name="finance_revenues_list.html", context=context
    )


@validate_session
def finance_view(request) -> HttpResponse:
    client = FinanceAPIClient()
    context = {}
    month = request.session.get("finance_month", datetime.today().date().month)
    year = request.session.get("finance_year", datetime.today().date().year)

    response = client.get_finance_data(request, month, year)

    if response.status_code == 200:
        context["data"] = response.json()
    elif response.status_code == 403:
        messages.error(request, f"{response.json()['detail']}", extra_tags="danger")
        return redirect("list_students")

    for field in context.get("data").get("values"):
        field["date"] = format_api_date(
            original_date_str=field["date"],
            original_format="%Y-%m-%d",
            desired_format="%d/%m de %Y",
        )

    for field in context.get("data").get("expense_list"):
        field["expense_date"] = format_api_date(
            original_date_str=field["expense_date"],
            original_format="%Y-%m-%d",
            desired_format="%d/%m de %Y",
        )

    if request.method == "POST":
        if "month" in request.POST and "year" in request.POST:
            request.session["finance_month"] = request.POST["month"]
            request.session["finance_year"] = request.POST["year"]
            return redirect("finance")

        if request.POST.get("action") == "expenses":
            return expenses_list(request=request, context=context)

        if request.POST.get("action") == "revenues":
            return revenues_list(request=request, context=context)

        if "delete_expense" in request.POST:
            delete_expense = client.delete_finance_expense(
                request=request, expense_id=request.POST.get("delete_expense")
            )
            if delete_expense.status_code == 204:
                messages.success(request, "Despesa deletada com sucesso.")
            else:
                messages.error(
                    request,
                    f"Erro ao deletar {delete_expense.status_code}",
                    extra_tags="danger",
                )
            return redirect("finance")

    return render(request=request, template_name="finance.html", context=context)


@validate_session
def finance_expense_add(request):
    client = FinanceAPIClient()

    if request.method == "POST":
        expense_date = request.POST.get("expense_date")
        description = request.POST.get("description")
        value = request.POST.get("value")

        new_expense = client.create_finance_expense(
            request=request,
            description=description,
            value=value,
            expense_date=expense_date,
        )

        if new_expense.status_code == 201:
            messages.success(request, "Despesa adicionada com sucesso.")
            return redirect("finance")
        else:
            messages.error(request, f"Erro: {new_expense.json()}", extra_tags="danger")
    return render(request=request, template_name="finance_expense_add.html")
