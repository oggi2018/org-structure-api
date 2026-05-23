# Org Structure API

Тестовое задание: API организационной структуры на Django + DRF.

## Стек

- Python 3
- Django
- Django REST Framework
- PostgreSQL
- pytest
- Docker + docker-compose

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/oggi2018/org-structure-api.git
cd org-structure-api
```

### 2. Создать .env

Пример:

```env
SECRET_KEY=django-secret-key
DEBUG=True

POSTGRES_DB=org_structure
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Запуск контейнеров

```bash
docker compose up --build
```

### 4. Применить миграции

В новом терминале:

```bash
docker compose exec web python manage.py migrate
```

### 5. Запуск тестов

```bash
docker compose exec web pytest
```

## API

После запуска приложение доступно по адресу: http://localhost:8000/

### Departments

- `POST /departments/` Создать подразделение
- `GET /departments/{id}` Получить подразделение (детали + сотрудники + поддерево)
- `PATCH /departments/{id}` Изменить название или parent подразделения
- `DELETE /departments/{id}` Удалить подразделение (cascade/reassign)

### Employees

- `POST /departments/{id}/employees/` Создать сотрудника в подразделении

## Особенности

- древовидная структура подразделений;
- защита от циклов;
- cascade/reassign удаление;
- PostgreSQL;
- запуск через Docker + docker-compose

## Дополнительно

- тесты на pytest
- автоматическая OpenAPI-схема через Django REST Framework
- встроенный DRF web-интерфейс API

## Автор
- Олег Генин
- [oleggenin@yandex.ru](mailto:oleggenin@yandex.ru)
- [Telegram: @Oleg_Genin](https://t.me/Oleg_Genin)