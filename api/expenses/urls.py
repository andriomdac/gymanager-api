from django.urls import path

from expenses.views import ExpenseDeleteAPIView, ExpensesAPIView


urlpatterns = [
    path("", ExpensesAPIView.as_view(), name="expenses"),
    path("<int:expense_id>/", ExpenseDeleteAPIView.as_view(), name="expense_delete"),
]
