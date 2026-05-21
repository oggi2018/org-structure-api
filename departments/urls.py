from django.urls import path

from .views import DepartmentCreateView, EmployeeCreateView


urlpatterns = [
    path(
        'departments/',
        DepartmentCreateView.as_view()
    ),
    path(
        'departments/<int:department_id>/employees/',
        EmployeeCreateView.as_view(),
    ),
]
