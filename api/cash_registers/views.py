from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.utils.exceptions import CustomValidatorException
from gyms.models import Gym
from .serializers import CashRegisterSerializer, CashRegisterDetailSerializer
from .models import CashRegister
from app.utils.paginator import paginate_serializer
from rest_framework.pagination import PageNumberPagination
from .utils import build_cash_resgister_serializer
from app.utils.permissions import AllowRoles
from datetime import datetime


class CashRegisterOpenTodayRegisterAPIView(APIView):
    def get_permissions(self):
        return [AllowRoles(["staff", "manager"])]

    def post(
        self,
        request,
    ):
        today = datetime.today().date()
        gym_id = request.user.profile.gym.id
        if not CashRegister.objects.filter(
            register_date=today, gym__id=gym_id
        ).exists():
            response = CashRegister.objects.create(
                register_date=today, gym=Gym.objects.get(id=gym_id)
            )
            serializer = CashRegisterSerializer(response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)


class CashRegisterListOpenRegistersOnly(APIView):
    def get_permissions(self):
        return [AllowRoles(["manager"])]

    def get(
        self,
        request: Request,
    ) -> Response:
        gym_id = request.user.profile.gym.id
        registers = CashRegister.objects.filter(gym=gym_id, is_opened=True).order_by(
            "-register_date"
        )
        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=registers,
            request=request,
            serializer=CashRegisterSerializer,
            paginator=paginator,
        )
        return paginator.get_paginated_response(serializer.data)


class CashRegisterListCreate(APIView):
    def get_permissions(self):
        return [AllowRoles(["manager"])]

    def get(
        self,
        request: Request,
    ) -> Response:
        gym_id = request.user.profile.gym.id

        month = request.GET.get("month")
        year = request.GET.get("year")
        if month and year:
            registers = CashRegister.objects.filter(
                gym=gym_id, register_date__month=month, register_date__year=year
            ).order_by("-register_date")
        else:
            registers = CashRegister.objects.filter(gym=gym_id).order_by(
                "-register_date"
            )

        paginator = PageNumberPagination()
        serializer = paginate_serializer(
            queryset=registers,
            request=request,
            serializer=CashRegisterSerializer,
            paginator=paginator,
        )
        return paginator.get_paginated_response(serializer.data)

    def post(
        self,
        request: Request,
    ) -> Response:
        try:
            gym_id = request.user.profile.gym.id
            data = request.data
            serializer = CashRegisterSerializer(data=data)
            serializer = build_cash_resgister_serializer(
                serializer_instance=serializer, gym_id=gym_id
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomValidatorException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class CashRegisterClose(APIView):
    def get_permissions(self):
        return [AllowRoles(["manager"])]

    def post(self, request: Request, register_id: str) -> Response:
        gym_id = request.user.profile.gym.id
        register = CashRegister.objects.get(id=register_id, gym__id=gym_id)
        serializer = CashRegisterSerializer(instance=register)

        if register.is_opened:
            register.is_opened = False
            register.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            data={"detail": "Caixa já fechado, alterações não são mais permitidas."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CashRegisterDetail(APIView):
    def get_permissions(self):
        return [AllowRoles(["manager"])]

    def get(self, request: Request, register_id: str) -> Response:
        gym_id = request.user.profile.gym.id
        register = CashRegister.objects.get(id=register_id, gym__id=gym_id)
        serializer = CashRegisterDetailSerializer(instance=register)
        return Response(serializer.data, status=status.HTTP_200_OK)
