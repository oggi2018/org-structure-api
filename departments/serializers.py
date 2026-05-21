from rest_framework import serializers

from .models import Department, Employee


class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'parent',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate_name(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Department name cannot be empty.'
            )

        return value


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'department',
            'full_name',
            'position',
            'hired_at',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate_full_name(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Full name cannot be empty.'
            )

        return value

    def validate_position(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Position cannot be empty.'
            )

        return value


class DepartmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'name',
            'parent',
        ]

    def validate_name(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Department name cannot be empty.'
            )

        return value