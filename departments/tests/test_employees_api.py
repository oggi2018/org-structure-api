import pytest


@pytest.mark.django_db
def test_create_employee(api_client, department):
    """Создание сотрудника в существующем подразделении."""

    response = api_client.post(
        f'/departments/{department.id}/employees/',
        {
            'full_name': 'Диззи Гиллеспи',
            'position': 'Backend разработчик',
        },
        format='json',
    )

    assert response.status_code == 201
    assert response.data['full_name'] == 'Диззи Гиллеспи'
    assert response.data['position'] == 'Backend разработчик'
    assert response.data['department'] == department.id
