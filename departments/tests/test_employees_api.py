import pytest
from rest_framework.test import APIClient

from departments.models import Department


@pytest.mark.django_db
def test_create_employee():
    """Создание сотрудника в существующем подразделении."""
    client = APIClient()
    department = Department.objects.create(name='Разработка')

    response = client.post(
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
