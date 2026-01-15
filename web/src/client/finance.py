import requests as rq
from ._base import BASE_URL
from utils.http import build_api_headers


class FinanceAPIClient:
    def __init__(self) -> None:
        self._base_url = f"{BASE_URL}/finance"

    def get_finance_data(self, request, month, year) -> rq.Response:
        return rq.api.get(
            url=f"{self._base_url}/?month={month}&year={year}",
            headers=build_api_headers(request=request),
        )

    def delete_finance_expense(self, request, expense_id) -> rq.Response:
        return rq.api.delete(
            url=f"{self._base_url}/expenses/{expense_id}/",
            headers=build_api_headers(request=request),
        )

    def create_finance_expense(
        self, request, description, value, expense_date
    ) -> rq.Response:
        data = {}
        if expense_date:
            data["expense_date"] = expense_date
        data["description"] = description
        data["value"] = value

        return rq.api.post(
            url=f"{self._base_url}/expenses/",
            headers=build_api_headers(request),
            json=data,
        )
