from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.views import APIView, Request, Response, status
from app.utils.paginator import paginate_serializer
from expenses.builders import build_request_data
from expenses.serializers import ExpenseSerializer
from .models import Expense
from app.utils.permissions import AllowRoles


class ExpensesAPIView(APIView):
    def get_permissions(self):
        return [
            AllowRoles(
                [
                    "manager",
                ]
            )
        ]

    def get(self, request: Request) -> Response:
        gym_id = request.user.profile.gym.id
        month = request.GET.get("month")
        year = request.GET.get("year")
        if month and year:
            expenses = Expense.objects.filter(
                expense_date__month=month, expense_date__year=year, gym__id=gym_id
            )
        else:
            expenses = Expense.objects.filter(
                expense_date__month=datetime.today().date().month, gym__id=gym_id
            )
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=expenses,
            request=request,
            serializer=ExpenseSerializer,
            paginator=paginator,
        )

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        data = build_request_data(request)
        serializer = ExpenseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDeleteAPIView(APIView):
    def delete(self, request, expense_id):
        gym_id = request.user.profile.gym.id
        if Expense.objects.filter(id=expense_id, gym__id=gym_id).exists():
            expense = Expense.objects.get(id=expense_id, gym__id=gym_id)
            expense.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
