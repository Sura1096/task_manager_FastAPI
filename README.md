# Диспетчер задач FastAPI

## Описание ✏️

Диспетчер задач FastAPI — это простой API управления задачами, созданный с использованием FastAPI. 
Он обеспечивает базовые операции CRUD (создание, чтение, обновление, удаление) для задач.

Проект также включает в себя аутентификацию JWT для защиты конечных точек API и интеграцию с базой данных PostgreSQL
с помощью SQLAlchemy.


## Функционал 🛠

- Регистрация и аутентификация пользователей;


- Аутентификация OAuth2 для доступа к API;


- Операции CRUD для задач (создание, чтение, обновление, удаление).


## Технологии ⚙️
* *Python* 
* *FastAPI*
* *Pydantic*
* *PyJWT*
* *PostgreSQL*
* *SQLAlchemy*
* *Alembic*

## Запуск 🚀 

1. Клонировать проект на свою локальную машину:

    ```bash
    git clone https://github.com/Sura1096/task_manager_FastAPI.git  # HTTPS
    ```

    ```bash
    git clone git@github.com:Sura1096/task_manager_FastAPI.git  # SSH
    ```
2. В корне проекта создать для проекта виртуальное окружение:

    ```bash
    python3.11 -m venv venv
    ```
   
3. Активировать виртуальное окружение:

   ```bash
    source venv/bin/activate  # Linux (Ubuntu)
    ```

4. Установить зависимости (находясь в виртуальном окружении проекта):

   ```bash
    pip install -r requirements.txt
    ```
   
5. В корне проекта создать файл *.env* и заполнить как в файле *.env.example*

6. Инициировать alembic баш-командой (находясь в папке проекта):
   ```bash
    alembic init alembic
    ```
   
7. Настроить файлы: alembic.ini, env.py (в папке alembic).

8. Создать миграцию с помощью команды:

   ```bash
    alembic revision --autogenerate -m '<Initial>'
    ```
9. Применить миграцию с помощью команды:

   ```bash
    alembic upgrade head
    ```

10. Запуск проекта через файл main.py



## API Endpoints

- `POST /auth/register/`: Регистрация нового пользователя;
- `POST /auth/login/`: Аутентификация и получение JWT токена;
- `GET /tasks/get_task/{task_id}/`: Получение информации о задаче по его id;
- `POST /tasks/add_task/`: Добаление новой задачи;
- `PUT /tasks/update_task/`: Обновление ифнормации задачи;
- `DELETE /tasks/delete_task/{task_id}/`: Удаление задачи по его id.


## Тестирование API с помощью Swagger UI
- После запуска API доступ к пользовательскому интерфейсу Swagger можно получить по следующему URL-адресу:

```bash
http://localhost:8000/docs
```

- Изучите доступные конечные точки и выберите ту, которую хотите протестировать.
- Нажмите кнопку **«Try it out»**, чтобы открыть интерактивную форму, в которую вы можете ввести данные.
- Заполните необходимые параметры и тело запроса (если применимо) согласно документации API, приведенной выше.
- Нажмите кнопку **«Execute»**, чтобы отправить запрос в API.
- Ответ будет отображен ниже, показывая код состояния и данные ответа.

*Вы также можете просмотреть примеры полезных данных запроса и ответа, которые могут быть полезны для 
понимания ожидаемого формата данных.*
