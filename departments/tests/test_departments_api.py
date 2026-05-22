import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_department():
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
