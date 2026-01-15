from datetime import datetime
from icecream import ic
from rest_framework.request import Request


def build_request_data(request: Request):
    data = request.data
    data["gym"] = request.user.profile.gym.id
    data["registered_by"] = request.user.username
    if "expense_date" not in data:
        data["expense_date"] = datetime.today().date()
    else:
        data["expense_date"] = datetime.strptime(
            data["expense_date"], "%Y-%m-%d"
        ).date()
    return data
