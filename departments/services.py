from rest_framework.exceptions import ValidationError

from .models import Department

DEPARTMENT_SELF_PARENT_ERROR = 'Подразделение не может быть родителем себя.'
DEPARTMENT_CYCLE_ERROR = 'Нельзя переместить подразделение внутрь поддерева.'


def validate_department_parent(
    department: Department,
    new_parent: Department | None,
) -> None:
    """Проверяет, что новый parent не создаёт цикл в дереве."""
    if new_parent is None:
        return
    if new_parent.id == department.id:
        raise ValidationError(DEPARTMENT_SELF_PARENT_ERROR)
    current_parent = new_parent.parent
    while current_parent is not None:
        if current_parent.id == department.id:
            raise ValidationError(DEPARTMENT_CYCLE_ERROR)
        current_parent = current_parent.parent
