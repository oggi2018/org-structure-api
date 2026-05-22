import pytest
from rest_framework.test import APIClient

from departments.models import Department, Employee


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def department(db):
    return Department.objects.create(
        name='Разработка',
    )


@pytest.fixture
def parent_department(db):
    return Department.objects.create(
        name='Компания',
    )


@pytest.fixture
def child_department(db, department):
    return Department.objects.create(
        name='Backend',
        parent=department,
    )


@pytest.fixture
def department_employee(db, department):
    return Employee.objects.create(
        department=department,
        full_name='Диззи Гиллеспи',
        position='Backend разработчик',
    )

