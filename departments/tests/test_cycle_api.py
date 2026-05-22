import pytest

from departments.models import Department


@pytest.mark.django_db
def test_move_department_to_itself(api_client, department):
    """Нельзя сделать подразделение родителем самого себя."""
    response = api_client.patch(
        f'/departments/{department.id}/',
        {
            'parent_id': department.id,
        },
        format='json',
    )

    assert response.status_code in (400, 409)


@pytest.mark.django_db
def test_move_department_inside_own_subtree(api_client):
    """Нельзя переместить подразделение внутрь собственного поддерева."""
    root_department = Department.objects.create(
        name='Company',
    )
    child_department = Department.objects.create(
        name='Backend',
        parent=root_department,
    )
    grandchild_department = Department.objects.create(
        name='Testing',
        parent=child_department,
    )

    response = api_client.patch(
        f'/departments/{root_department.id}/',
        {
            'parent_id': grandchild_department.id,
        },
        format='json',
    )

    assert response.status_code in (400, 409)
