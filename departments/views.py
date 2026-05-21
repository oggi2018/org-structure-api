from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department
from .serializers import DepartmentCreateSerializer, EmployeeCreateSerializer


class DepartmentCreateView(APIView):
    def post(self, request):
        serializer = DepartmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = serializer.save()

        return Response(
            DepartmentCreateSerializer(department).data,
            status=status.HTTP_201_CREATED,
        )


class EmployeeCreateView(APIView):
    def post(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)
        serializer = EmployeeCreateSerializer(
            data={**request.data, 'department': department.id}
        )
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()
        return Response(
            EmployeeCreateSerializer(employee).data,
            status=status.HTTP_201_CREATED,
        )
