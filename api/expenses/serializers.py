from icecream import ic
from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"

    def validate_description(self, value):
        expense_date = self.initial_data.get("expense_date")
        description = value

        if Expense.objects.filter(
            expense_date__month=expense_date.month,
            expense_date__day=expense_date.day,
            description=description,
        ).exists():
            raise serializers.ValidationError(
                "Já existe uma despesa com essa descrição para hoje, utilize outra descrição."
            )
        return value
