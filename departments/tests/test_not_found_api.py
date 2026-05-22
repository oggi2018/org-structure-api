import pytest


@pytest.mark.django_db
def test_get_nonexistent_department(api_client):
    """Ошибка при запросе несуществующего подразделения."""
    response = api_client.get('/departments/XXX/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_patch_nonexistent_department(api_client):
    """Ошибка при изменении несуществующего подразделения."""
    response = api_client.patch(
        '/departments/XXX/',
        {
            'name': 'Backend',
        },
        format='json',
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_nonexistent_department(api_client):
    """Ошибка при удалении несуществующего подразделения."""
    response = api_client.delete(
        '/departments/XXX/?mode=cascade',
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_create_employee_in_nonexistent_department(api_client):
    """Ошибка при создании сотрудника в несуществующем подразделении."""
    response = api_client.post(
        '/departments/XXX/employees/',
        {
            'full_name': 'Диззи Гиллеспи',
            'position': 'Backend разработчик',
        },
        format='json',
    )

    assert response.status_code == 404
