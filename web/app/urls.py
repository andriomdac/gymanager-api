from django.urls import path

from views.finance import finance_expense_add, finance_view
from views.student import (
    add_payment,
    add_value,
    delete_student,
    detail_student,
    list_students,
    add_student,
    update_student,
)
from views.register import (
    close_register,
    detail_register,
    list_registers,
    open_register,
    redo_payment,
)
from views.session import (
    login,
    logout,
)
from views.home import homepage


urlpatterns = [
    path("", homepage, name="homepage"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("add-student/", add_student, name="add_student"),
    path("list-students/", list_students, name="list_students"),
    path("detail-student/<int:student_id>/", detail_student, name="detail_student"),
    path(
        "detail-student/<int:student_id>/update/", update_student, name="update_student"
    ),
    path("detail-student/<int:student_id>/payment/", add_payment, name="add_payment"),
    path("delete-student/<int:student_id>/", delete_student, name="delete_student"),
    path(
        "detail-student/<int:student_id>/payment/<int:payment_id>/add-value/",
        add_value,
        name="add_value",
    ),
    path("cash-registers/", list_registers, name="list_registers"),
    path("open-register/", open_register, name="open_register"),
    path("detail-register/<int:register_id>/", detail_register, name="detail_register"),
    path(
        "detail-register/<int:register_id>/student/<int:student_id>/payment/<int:payment_id>/",
        redo_payment,
        name="redo_payment",
    ),
    path("close-register/<int:register_id>/", close_register, name="close_register"),
    path("finance/", finance_view, name="finance"),
    path("finance/create-expense/", finance_expense_add, name="create-expense"),
]
