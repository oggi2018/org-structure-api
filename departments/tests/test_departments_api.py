import pytest
from rest_framework.test import APIClient

from departments.models import Department, Employee


@pytest.mark.django_db
def test_create_department():
    """Создание корневого подразделения без parent_id."""
    client = APIClient()

    response = client.post(
        '/departments/',
        {
            'name': 'Отдел тестирования ПО',
        },
        format='json',
    )

    assert response.status_code == 201
    assert response.data['name'] == 'Отдел тестирования ПО'
    assert response.data['parent_id'] is None


@pytest.mark.django_db
def test_create_child_department():
    """Создание дочернего подразделения с parent_id."""
    client = APIClient()
    parent = Department.objects.create(
        name='Разработка',
    )

    response = client.post(
        '/departments/',
        {
            'name': 'Backend',
            'parent_id': parent.id,
        },
        format='json',
    )

    assert response.status_code == 201
    assert response.data['name'] == 'Backend'
    assert response.data['parent_id'] == parent.id


@pytest.mark.django_db
def test_get_department_tree():
    """Получение подразделения вместе с сотрудниками и дочерними отделами."""
    client = APIClient()
    department = Department.objects.create(
        name='Разработка',
    )
    child = Department.objects.create(
        name='Backend',
        parent=department,
    )
    Employee.objects.create(
        department=department,
        full_name='Диззи Гиллеспи',
        position='Backend разработчик',
    )

    response = client.get(f'/departments/{department.id}/')

    assert response.status_code == 200
    assert response.data['department']['id'] == department.id
    assert response.data['department']['name'] == 'Разработка'
    assert len(response.data['employees']) == 1
    assert response.data['employees'][0]['full_name'] == 'Диззи Гиллеспи'
    assert len(response.data['children']) == 1
    assert response.data['children'][0]['department']['id'] == child.id


@pytest.mark.django_db
def test_rename_department():
    """Изменение названия подразделения."""
    client = APIClient()
    department = Department.objects.create(name='Разработка')

    response = client.patch(
        f'/departments/{department.id}/',
        {
            'name': 'Backend',
        },
        format='json',
    )
    department.refresh_from_db()

    assert response.status_code == 200
    assert department.name == 'Backend'


@pytest.mark.django_db
def test_move_department_to_another_parent():
    """Перемещение подразделения в другой родительский отдел."""
    client = APIClient()
    root = Department.objects.create(name='Компания')
    department = Department.objects.create(name='Разработка')

    response = client.patch(
        f'/departments/{department.id}/',
        {
            'parent_id': root.id,
        },
        format='json',
    )
    department.refresh_from_db()

    assert response.status_code == 200
    assert response.data['parent_id'] == root.id
    assert department.parent_id == root.id
