from django.urls import path

from finance.views import MonthRevenues


urlpatterns = [
    path("", MonthRevenues.as_view(), name="month-revenues"),
]
