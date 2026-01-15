from django.contrib import admin
from expenses.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = [
        "expense_date",
        "description",
        "registered_by",
        "value",
        "created_at",
    ]
