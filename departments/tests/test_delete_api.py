import pytest

from departments.models import Department, Employee


@pytest.mark.django_db
def test_delete_department_cascade(
    api_client,
    department,
    child_department,
    department_employee,
):
    """Cascade удаляет подразделение вместе с дочерними и сотрудниками."""
    response = api_client.delete(
        f'/departments/{department.id}/?mode=cascade',
    )
    assert response.status_code == 204
    assert not Department.objects.filter(id=department.id).exists()
    assert not Department.objects.filter(id=child_department.id).exists()
    assert not Employee.objects.filter(id=department_employee.id).exists()


@pytest.mark.django_db
def test_delete_department_reassign(
    api_client,
    department,
    child_department,
    department_employee,
    parent_department,
):
    """Reassign переносит сотрудников и дочерние отделы."""
    response = api_client.delete(
        (
            f'/departments/{department.id}/'
            f'?mode=reassign'
            f'&reassign_to_department_id={parent_department.id}'
        ),
    )
    child_department.refresh_from_db()
    department_employee.refresh_from_db()

    assert response.status_code == 204
    assert not Department.objects.filter(id=department.id).exists()
    assert child_department.parent_id == parent_department.id
    assert department_employee.department_id == parent_department.id
