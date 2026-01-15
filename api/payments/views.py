from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from app.utils.exceptions import CustomValidatorException
from students.models import Student
from students.validators import validate_student
from .models import Payment, PaymentValue
from .serializers import (
    PaymentSerializer,
    PaymentValueSerializer,
    PaymentDetailSerializer,
)
from .validators import (
    validate_payment_deletion,
    validate_payment_value_serializer,
    validate_payment_serializer,
)
from .serializer_builders import build_payment_serializer
from app.utils.paginator import paginate_serializer
from rest_framework.pagination import PageNumberPagination
from cash_registers.utils import update_cash_register_amount
from app.utils.permissions import AllowRoles


class PaymentsListCreateAPIView(APIView):
    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def get(self, request: Request, student_id: int) -> Response:
        gym_id = request.user.profile.gym.id
        student = validate_student(student_id=student_id, gym_id=gym_id)
        student_payments = student.payments.all().order_by("-next_payment_date")

        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=student_payments,
            request=request,
            serializer=PaymentDetailSerializer,
            paginator=paginator,
        )

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request, student_id: int) -> Response:
        try:
            gym_id = request.user.profile.gym.id
            serializer = PaymentSerializer(data=request.data)
            serializer = build_payment_serializer(
                request,
                serializer=serializer,
                student_id=student_id,
            )
            if serializer.is_valid():
                validate_payment_serializer(
                    serializer=serializer, student_id=student_id
                )
                serializer.save()
                update_cash_register_amount(serializer.data["cash_register"])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailDeleteAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowRoles(["staff", "manager"])]
        if self.request.method == "DELETE":
            return [AllowRoles(["manager", "staff"])]
        return [AllowRoles()]

    def get(
        self,
        request: Request,
        payment_id: int,
        student_id: int,
    ) -> Response:
        gym_id = request.user.profile.gym.id
        payment = Payment.objects.get(id=payment_id, student__gym__id=gym_id)
        serializer = PaymentDetailSerializer(instance=payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, payment_id: int, student_id: int) -> Response:
        try:
            gym_id = request.user.profile.gym.id
            payment = Payment.objects.get(id=payment_id, student__gym__id=gym_id)
            payment = validate_payment_deletion(request=request, payment=payment)
            payment.delete()
            update_cash_register_amount(register_id=payment.cash_register.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentValuesListCreateAPIView(APIView):
    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def get(
        self,
        request: Request,
        student_id: int,
        payment_id: int,
    ) -> Response:
        gym_id = request.user.profile.gym.id
        payment = Payment.objects.get(id=payment_id, student__gym__id=gym_id)
        values = payment.payment_values.all()

        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=values,
            request=request,
            serializer=PaymentValueSerializer,
            paginator=paginator,
        )

        return paginator.get_paginated_response(serializer.data)

    def post(
        self,
        request: Request,
        student_id: int,
        payment_id: int,
    ) -> Response:
        try:
            gym_id = request.user.profile.gym.id
            data = request.data
            payment = Payment.objects.get(id=payment_id, student__gym__id=gym_id)
            serializer = PaymentValueSerializer(data=data)
            serializer = validate_payment_value_serializer(
                serializer=serializer, payment_id=payment_id
            )
            if serializer.is_valid():
                serializer.save()
                update_cash_register_amount(register_id=payment.cash_register.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentValueDeleteAPIView(APIView):
    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def delete(
        self, request: Request, student_id: int, payment_id: int, value_id: int
    ) -> Response:
        gym_id = request.user.profile.gym.id
        value = PaymentValue.objects.get(
            id=value_id, payment__id=payment_id, payment__student__gym__id=gym_id
        )
        value.delete()
        update_cash_register_amount(register_id=value.payment.cash_register.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentValuesDeleteAllAPIView(APIView):
    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def delete(self, request: Request, student_id: int, payment_id: int) -> Response:
        gym_id = request.user.profile.gym.id
        payment = Payment.objects.get(id=payment_id, student__gym__id=gym_id)
        values = payment.payment_values.all()
        if values:
            for value in values:
                value.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProofOfPaymentAPIView(APIView):
    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def get(self, request, student_id, payment_id):
        gym_id = request.user.profile.gym.id
        payment = Payment.objects.get(id=payment_id, student__gym__id=gym_id)

        total_value = 0
        for value in payment.payment_values.all():
            total_value += value.value

        data = {
            "title": "Comprovante de Pagamento",
            "student": {
                "id": payment.student.id,
                "name": payment.student.name,
                "phone": payment.student.phone,
            },
            "payment_date": payment.payment_date,
            "next_payment_date": payment.next_payment_date,
            "payment_package": payment.payment_package.name,
            "total_value": total_value,
            "receiver": payment.receiver,
            "gym": payment.student.gym.name,
        }
        return Response(data=data)
