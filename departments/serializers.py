from rest_framework import serializers

from .models import Department, Employee


DEPARTMENT_NAME_EMPTY = 'Название подразделения не может быть пустым.'
DEPARTMENT_ALREADY_EXISTS = 'Подразделение с таким именем уже существует.'
FULL_NAME_EMPTY = 'ФИО не может быть пустым.'
POSITION_EMPTY = 'Должность не может быть пустой.'

MAX_DEPARTMENT_DEPTH = 5
DEFAULT_DEPARTMENT_DEPTH = 1
MIN_DEPARTMENT_DEPTH = 0

DELETE_MODE_CASCADE = 'cascade'
DELETE_MODE_REASSIGN = 'reassign'
DELETE_MODE_REQUIRED_ERROR = 'Некорректный режим удаления.'
REASSIGN_DEPARTMENT_REQUIRED_ERROR = 'reassign_to_department_id обязателен'


class DepartmentParentIdMixin(serializers.Serializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent',
        queryset=Department.objects.all(),
        required=False,
        allow_null=True,
    )


class DepartmentCreateSerializer(
    DepartmentParentIdMixin,
    serializers.ModelSerializer
):
    class Meta:
        model = Department
        fields = ['id', 'name', 'parent_id', 'created_at']
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


class DepartmentUpdateSerializer(
    DepartmentParentIdMixin,
    serializers.ModelSerializer
):
    class Meta:
        model = Department
        fields = ['name', 'parent_id']

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


class DepartmentTreeQuerySerializer(serializers.Serializer):
    depth = serializers.IntegerField(
        required=False,
        default=DEFAULT_DEPARTMENT_DEPTH,
        min_value=MIN_DEPARTMENT_DEPTH,
        max_value=MAX_DEPARTMENT_DEPTH,
    )
    include_employees = serializers.BooleanField(
        required=False,
        default=True,
    )


class DepartmentDeleteQuerySerializer(serializers.Serializer):
    mode = serializers.ChoiceField(
        choices=[DELETE_MODE_CASCADE, DELETE_MODE_REASSIGN],
        required=True,
        error_messages={'invalid_choice': DELETE_MODE_REQUIRED_ERROR},
    )
    reassign_to_department_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        mode = attrs.get('mode')
        reassign_to_department_id = attrs.get('reassign_to_department_id')
        if (
            mode == DELETE_MODE_REASSIGN
            and reassign_to_department_id is None
        ):
            raise serializers.ValidationError(
                REASSIGN_DEPARTMENT_REQUIRED_ERROR,
            )

        return attrs
