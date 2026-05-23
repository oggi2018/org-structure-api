import pytest

from departments.models import MAX_TEXT_LENGTH


@pytest.mark.django_db
def test_create_department_with_empty_name(api_client):
    """Ошибка при создании подразделения с пустым названием."""
    response = api_client.post(
        '/departments/',
        {
            'name': '',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'name' in response.data


@pytest.mark.django_db
def test_create_department_with_blank_name(api_client):
    """Ошибка при создании подразделения из пробелов."""
    response = api_client.post(
        '/departments/',
        {
            'name': '   ',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'name' in response.data


@pytest.mark.django_db
def test_create_duplicate_department_name(api_client, department):
    """Нельзя создать одинаковые подразделения у одного parent."""
    response = api_client.post(
        '/departments/',
        {
            'name': 'Разработка',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'non_field_errors' in response.data


@pytest.mark.django_db
def test_create_same_department_name_in_another_parent(
    api_client,
    parent_department,
):
    """Одинаковые названия допустимы в разных parent."""
    response = api_client.post(
        '/departments/',
        {
            'name': 'Компания',
            'parent_id': parent_department.id,
        },
        format='json',
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_employee_with_empty_full_name(api_client, department):
    """Ошибка при созданении сотрудника с пустым full_name."""
    response = api_client.post(
        f'/departments/{department.id}/employees/',
        {
            'full_name': '',
            'position': 'Backend разработчик',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'full_name' in response.data


@pytest.mark.django_db
def test_create_employee_with_empty_position(api_client, department):
    """Ошибка при создании сотрудника с пустым position."""
    response = api_client.post(
        f'/departments/{department.id}/employees/',
        {
            'full_name': 'Диззи Гиллеспи',
            'position': '',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'position' in response.data


@pytest.mark.django_db
def test_create_employee_with_blank_fields(api_client, department):
    """Ошибка при создании сотрудника из пробелов."""

    response = api_client.post(
        f'/departments/{department.id}/employees/',
        {
            'full_name': '   ',
            'position': '   ',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'full_name' in response.data
    assert 'position' in response.data


@pytest.mark.django_db
def test_create_department_with_too_long_name(api_client):
    """Ошибка при создании подразделения со слишком длинным названием."""
    response = api_client.post(
        '/departments/',
        {
            'name': 'A' * (MAX_TEXT_LENGTH + 1),
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'name' in response.data


@pytest.mark.django_db
def test_create_employee_with_too_long_full_name(api_client, department):
    """Ошибка при создании сотрудника со слишком длинным full_name."""
    response = api_client.post(
        f'/departments/{department.id}/employees/',
        {
            'full_name': 'A' * (MAX_TEXT_LENGTH + 1),
            'position': 'Backend разработчик',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'full_name' in response.data


@pytest.mark.django_db
def test_create_employee_with_too_long_position(api_client, department):
    """Ошибка при создании сотрудника со слишком длинным position."""
    response = api_client.post(
        f'/departments/{department.id}/employees/',
        {
            'full_name': 'Диззи Гиллеспи',
            'position': 'A' * (MAX_TEXT_LENGTH + 1),
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'position' in response.data
