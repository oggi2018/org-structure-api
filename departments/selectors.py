from .models import Department


def get_department_by_id(department_id: int) -> Department | None:
    return Department.objects.filter(id=department_id).first()


def build_department_tree(
    department: Department,
    depth: int,
    include_employees: bool,
) -> dict:
    result = {
        'department': {
            'id': department.id,
            'name': department.name,
            'parent': department.parent_id,
            'created_at': department.created_at,
        },
        'employees': [],
        'children': [],
    }
    if include_employees:
        result['employees'] = [
            {
                'id': employee.id,
                'department': employee.department_id,
                'full_name': employee.full_name,
                'position': employee.position,
                'hired_at': employee.hired_at,
                'created_at': employee.created_at,
            }
            for employee in department.employees.all()
        ]
    if depth <= 0:
        return result
    result['children'] = [
        build_department_tree(
            child,
            depth=depth - 1,
            include_employees=include_employees,
        )
        for child in department.children.all()
    ]
    return result
