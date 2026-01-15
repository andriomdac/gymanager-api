from django.http import JsonResponse
from rest_framework.views import APIView, Response
from cash_registers.models import CashRegister
from expenses.models import Expense
from app.utils.permissions import AllowRoles


class MonthRevenues(APIView):
    def get_permissions(self):
        return [
            AllowRoles(
                [
                    "manager",
                ]
            )
        ]

    def get(self, request):
        gym_id = request.user.profile.gym.id
        month = request.GET.get("month")
        year = request.GET.get("year")
        data = {}
        values = []
        data["month"] = month
        data["year"] = year

        registers = CashRegister.objects.filter(
            register_date__month=month, register_date__year=year, gym__id=gym_id
        )
        expenses = Expense.objects.filter(
            expense_date__month=month, expense_date__year=year, gym__id=gym_id
        )

        total_month_revenues = 0
        for register in registers:
            for payment in register.payments.all():
                for value in payment.payment_values.all():
                    values.append(
                        {
                            "date": register.register_date,
                            "method": value.payment_method.name,
                            "value": value.value,
                        },
                    )
                    total_month_revenues += value.value

        total_expenses = 0
        expense_list = []
        for expense in expenses:
            expense_list.append(
                {
                    "id": expense.id,
                    "expense_date": expense.expense_date,
                    "description": expense.description,
                    "value": expense.value,
                    "registered_by": expense.registered_by,
                }
            )
            total_expenses += expense.value

        net_profit = total_month_revenues - total_expenses

        data["expense_list"] = expense_list
        data["total_expense"] = total_expenses
        data["total_month_revenue"] = total_month_revenues
        data["net_profit"] = net_profit
        data["values"] = values

        return Response(data=data, status=200)
