# FastAPI 

## 1. Установка и настройка окружения

### Создать и активировать виртуальное окружение:

#### Windows (PowerShell):
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

#### Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Установка зависимостей:
```bash
pip install -r requirements.txt
```

### Создание .env файла (если его нет):
APP_HOST=127.0.0.1
APP_PORT=8000
SECRET_KEY=secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440

## 2. Запуск сервера:
```bash
uvicorn main:app --reload
```

## 3. Проверка API:

http://127.0.0.1:8000/docs

Появится Swagger UI с эндпоинтами.

Redoc.

http://127.0.0.1:8000/redoc

## 4. Проверка использования:

1. Регистрация пользователя (POST /auth/register)

Команда для регистрации нового пользователя

POST /api/v1/auth/register

Пример запроса
```bash
http POST http://127.0.0.1:8000/api/v1/auth/register username="user1" email="user1@example.com" password="password"
```


2. Логин (POST /auth/login)

Команда для логина и получения токенов

Пример запроса
```bash
http POST http://127.0.0.1:8000/api/v1/auth/login username="user1" password="password"
```


3. Проверка списка пользователей (GET /users/)

Пример запроса
```bash
http GET http://127.0.0.1:8000/api/v1/users/ Authorization:"Bearer <ACCESS_TOKEN>"
```


4. Создание нескольких пользователей (POST /users/ и /users/bulk)

Создание одного пользователя:

Пример запроса
```bash
http POST http://127.0.0.1:8000/api/v1/users/ username="user2" email="user2@example.com" password="password123" Authorization:"Bearer <ACCESS_TOKEN>"
```

Создание нескольких пользователей (bulk):

Пример запроса
```bash
http POST http://127.0.0.1:8000/api/v1/users/bulk users:='[{"username":"user3", "email":"user3@example.com", "password":"password123"}, {"username":"user4", "email":"user4@example.com", "password":"password123"}]' Authorization:"Bearer <ACCESS_TOKEN>"
```


5. Обновление и удаление пользователей (PUT /users/{user_id} и DELETE /users/{user_id})

Обновление данных пользователя:

Пример запроса
```bash
http PUT http://127.0.0.1:8000/api/v1/users/2 username="newuser2" email="newuser2@example.com" Authorization:"Bearer <ACCESS_TOKEN>"
```

Удаление пользователя:

Пример запроса
```bash
http DELETE http://127.0.0.1:8000/api/v1/users/2 Authorization:"Bearer <ACCESS_TOKEN>"
```


6. Обновление токенов (POST /auth/refresh)

Команда для обновления токенов с использованием refresh_token:

Пример запроса
```bash
http POST http://127.0.0.1:8000/api/v1/auth/refresh refresh_token="<REFRESH_TOKEN>"
```

7. Повторный запрос с новым access_token

После того как получили новые токены, можно повторить запрос для получения списка пользователей с новым access_token:

Пример запроса
```bash
http GET http://127.0.0.1:8000/api/v1/users/ Authorization:"Bearer <NEW_ACCESS_TOKEN>"
```
