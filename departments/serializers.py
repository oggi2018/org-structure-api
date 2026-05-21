from rest_framework import serializers

from .models import Department, Employee


DEPARTMENT_NAME_EMPTY = 'Название подразделения не может быть пустым.'
DEPARTMENT_ALREADY_EXISTS = 'Подразделение с таким именем уже существует.'
FULL_NAME_EMPTY = 'ФИО не может быть пустым.'
POSITION_EMPTY = 'Должность не может быть пустой.'


class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError(DEPARTMENT_NAME_EMPTY)
        return value

    def validate(self, attrs):
        name = attrs.get('name')
        parent = attrs.get('parent')
        if Department.objects.filter(
            name=name,
            parent=parent,
        ).exists():
            raise serializers.ValidationError(DEPARTMENT_ALREADY_EXISTS)
        return attrs


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'department', 'full_name', 'position',
                  'hired_at', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_full_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError(FULL_NAME_EMPTY)
        return value

    def validate_position(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError(POSITION_EMPTY)
        return value


class DepartmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'parent']

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError(DEPARTMENT_NAME_EMPTY)
        return value

    def validate(self, attrs):
        name = attrs.get('name', self.instance.name)
        parent = attrs.get('parent', self.instance.parent)
        if Department.objects.filter(
            name=name,
            parent=parent,
        ).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError(DEPARTMENT_ALREADY_EXISTS)
        return attrs
