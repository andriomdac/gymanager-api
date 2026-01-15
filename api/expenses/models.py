from django.core.validators import MinValueValidator
from django.db import models
from gyms.models import Gym


class Expense(models.Model):
    gym = models.ForeignKey(to=Gym, on_delete=models.PROTECT, related_name="expenses")
    expense_date = models.DateField()
    description = models.CharField(max_length=500)
    registered_by = models.CharField(max_length=100)
    value = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
