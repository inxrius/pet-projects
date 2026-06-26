# Система аутентификации и авторизации

Backend-приложение с собственной системой аутентификации (JWT) и авторизации (RBAC) на Django REST Framework.

## Стек

- **Django** 5.2.15
- **Django REST Framework** 3.17.1
- **JWT** (SimpleJWT)
- **SQLite** (разработка) / **PostgreSQL** (продакшн)

## Быстрый старт

### 1. Установка зависимостей

```bash
python -m venv venv
venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary python-dotenv
```

### 2. Настройка

Создайте файл `.env`:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=effective_mobile_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 3. Миграции и тестовые данные

```bash
python manage.py migrate
python manage.py seed_data
```

### 4. Запуск сервера

```bash
python manage.py runserver
```

API доступно по адресу: `http://localhost:8000/api/`

## API Endpoints

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/auth/register/` | Регистрация |
| POST | `/api/auth/login/` | Вход (получение JWT) |
| POST | `/api/auth/logout/` | Выход |
| GET | `/api/auth/profile/` | Профиль |
| PUT | `/api/auth/profile/` | Обновление профиля |
| DELETE | `/api/auth/profile/` | Удаление аккаунта |

### Управление правами (только для админа)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET/POST | `/api/roles/` | Список/создание ролей |
| GET/PUT/DELETE | `/api/roles/{id}/` | Детали роли |
| GET/POST | `/api/resources/` | Список/создание ресурсов |
| GET/POST | `/api/permissions/` | Список/создание разрешений |
| GET/POST | `/api/user-roles/` | Назначение ролей пользователям |
| GET/POST | `/api/role-permissions/` | Назначение разрешений ролям |

### Mock-ресурсы

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/documents/` | Просмотр документов |
| POST | `/api/documents/` | Создание документа |
| GET | `/api/reports/` | Просмотр отчетов |
| POST | `/api/reports/` | Создание отчета |

## Примеры использования

### Вход в систему

```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Ответ:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin"
  }
}
```

### Доступ к защищенному ресурсу

```bash
GET /api/documents/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Тестовые аккаунты

После выполнения `python manage.py seed_data`:

| Роль | Email | Пароль | Права |
|------|-------|--------|-------|
| Admin | admin@example.com | admin123 | Все права |
| Manager | manager@example.com | manager123 | Документы и отчеты |
| User | user@example.com | user123 | Документы (просмотр, создание) |
| Guest | guest@example.com | guest123 | Только просмотр |

## Структура базы данных

### Основные таблицы

**users** - Пользователи системы
- email (уникальный)
- username, first_name, last_name
- password (хеш)
- is_active (мягкое удаление)

**roles** - Роли (Admin, Manager, User, Guest)
**resources** - Ресурсы (documents, reports, users, settings)
**permissions** - Разрешения (view, create, update, delete, export)

### Связи

```
User ── UserRole ── Role ── RolePermission ── Permission ── Resource
```

- Один пользователь может иметь несколько ролей
- Одна роль может иметь несколько разрешений
- Разрешение = действие (view/create/update/delete) на ресурсе

## Коды ответов

- **200** - Успешно
- **201** - Создано
- **401** - Не авторизован (нет токена или токен невалиден)
- **403** - Доступ запрещен (недостаточно прав)
- **404** - Не найдено

## Переключение на PostgreSQL

1. Установите PostgreSQL и создайте базу:
```sql
CREATE DATABASE effective_mobile_db;
```

2. Обновите `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'effective_mobile_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Выполните миграции:
```bash
python manage.py migrate
python manage.py seed_data
```

## Разработка

```bash
# Создание суперпользователя
python manage.py createsuperuser

# Доступ к админке
http://localhost:8000/admin/
```

## Лицензия

Образовательный проект