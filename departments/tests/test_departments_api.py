import pytest


@pytest.mark.django_db
def test_create_department(api_client):
    """Создание корневого подразделения без parent_id."""
    response = api_client.post(
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
def test_create_child_department(api_client, department):
    """Создание дочернего подразделения с parent_id."""
    response = api_client.post(
        '/departments/',
        {
            'name': 'Backend',
            'parent_id': department.id,
        },
        format='json',
    )

    assert response.status_code == 201
    assert response.data['name'] == 'Backend'
    assert response.data['parent_id'] == department.id


@pytest.mark.django_db
def test_get_department_tree(
    api_client, department,
    child_department,
    department_employee,
):
    """Получение подразделения вместе с сотрудниками и дочерними отделами."""
    response = api_client.get(f'/departments/{department.id}/')

    assert response.status_code == 200
    assert response.data['department']['id'] == department.id
    assert response.data['department']['name'] == 'Разработка'
    assert len(response.data['employees']) == 1
    assert response.data['employees'][0]['full_name'] == 'Диззи Гиллеспи'
    assert len(response.data['children']) == 1
    assert (
        response.data['children'][0]['department']['id']
        == child_department.id
    )


@pytest.mark.django_db
def test_rename_department(api_client, department):
    """Изменение названия подразделения."""
    response = api_client.patch(
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
def test_move_department_to_another_parent(
    api_client,
    parent_department,
    department,
):
    """Перемещение подразделения в другой родительский отдел."""
    response = api_client.patch(
        f'/departments/{department.id}/',
        {
            'parent_id': parent_department.id,
        },
        format='json',
    )
    department.refresh_from_db()

    assert response.status_code == 200
    assert response.data['parent_id'] == parent_department.id
    assert department.parent_id == parent_department.id
