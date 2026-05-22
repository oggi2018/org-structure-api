from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department
from .selectors import build_department_tree
from .serializers import (
    DELETE_MODE_CASCADE,
    DELETE_MODE_REASSIGN,
    DepartmentCreateSerializer,
    DepartmentTreeQuerySerializer,
    EmployeeCreateSerializer,
    DepartmentUpdateSerializer,
    DepartmentDeleteQuerySerializer,
)
from .services import (
    delete_department_cascade,
    delete_department_reassign,
    validate_department_parent,
)


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


class DepartmentDetailView(APIView):
    def get(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)
        query_serializer = DepartmentTreeQuerySerializer(
            data=request.query_params,
        )
        query_serializer.is_valid(raise_exception=True)
        data = build_department_tree(
            department=department,
            depth=query_serializer.validated_data['depth'],
            include_employees=query_serializer.validated_data[
                'include_employees'
            ],
        )
        return Response(data)

    def patch(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)
        serializer = DepartmentUpdateSerializer(
            department,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        new_parent = serializer.validated_data.get(
            'parent',
            department.parent,
        )
        validate_department_parent(
            department=department,
            new_parent=new_parent,
        )
        department = serializer.save()
        return Response(DepartmentCreateSerializer(department).data)

    def delete(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)
        query_serializer = DepartmentDeleteQuerySerializer(
            data=request.query_params,
        )
        query_serializer.is_valid(raise_exception=True)
        mode = query_serializer.validated_data['mode']
        if mode == DELETE_MODE_CASCADE:
            delete_department_cascade(department)
        elif mode == DELETE_MODE_REASSIGN:
            reassign_to_department = get_object_or_404(
                Department,
                id=query_serializer.validated_data['reassign_to_department_id']
            )
            delete_department_reassign(
                department=department,
                reassign_to_department=reassign_to_department,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
