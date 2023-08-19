
## Описание
### О проекте
Галера Яндекс практикума по поднятию навыков работы с DRF
```
        https://paymir121.ddns.net/
```
login nikox121
password 456852Zx
### Технологии
Python 3.7 Django 3.2.16

### Авторы
Nikki Nikonor и Яндекс Практикум

## Установка
Как развернуть проект на локальной машине;

### Клонирование репозитория:
Просите разрешение у владельца репозитория( можно со слезами на глазах)
Клонируете репозиторий:

```bash
        git clone  git@github.com:Paymir121/foodgram-project-react.git
```

### Cоздать и активировать виртуальное окружение:
```
python -m venv venv
* Если у вас Linux/macOS
    ```
    source venv/bin/activate
    ```

* Если у вас windows
    ```
    source venv/scripts/activate
    ```
```
### Установить зависимости из файла requirements.txt:
```
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
```


### Выполнить миграции:
```
        cd backend
        python manage.py makemigrations
        python manage.py migrate
```

### Запустить проект:
```
        cd backend
        python manage.py runserver
```

### Создать суперпользователя:
```
        cd backend
        python manage.py createsuperuser
```
### Наполнить базу данных:
```
        cd backend
        python manage.py importcsv
```

## Запуск докер контейнеров на локальной машине:

### Билдим проект и запускаем:
```
        docker compose up --build
```

### Выполнить миграции:
```
        docker compose exec backend python manage.py migrate
```

### Выполнить создание суперпользователя:
```
        docker compose exec backend python manage.py createsuperuser
```

### Выполнить Собрать статику Django:
```
        docker compose exec backend python manage.py collectstatic
        docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```

### Выполнить добавление ингредиентов из csv-файла:
```
        docker compose exec backend python manage.py importcsv
```

## Запуск докер контейнеров на удаленной машине:

### Выполнить обновление apt:
```
        sudo apt update
```

### Билдим проект и запускаем:
```
        sudo docker compose -f docker-compose.production.yml up --build
```

### Выполнить миграции:
```
        docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

### Выполнить миграции:
```
        docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

### Выполнить добавление ингредиентов из csv-файла:
```
        docker compose -f docker-compose.production.yml exec backend python manage.py importcsv
```


### Настройки nginx:
```
        sudo nano /etc/nginx/sites-enabled/default
```

## Примеры
Некоторые примеры запросов к API.

### Регистрация

#### Для смертных

##### End Point
```
POST  api/v1/auth/signup/
```
#####  Body
```
{
        "email": "paymisssr@kek.ru",
        "username": "passsymir121"
}
```
#### Для admin

#####  End Point
```
POST  api/users/
```
#####  Body
```
{
    "email": "nikox12@mail.ru",
    "username": "nikjox",
    "password": "456852Zx",
    "first_name": "kewk",
    "last_name": "wsq"
}
```
### Получение токена

##### End Point
```
POST  api/auth/token/
```
#####  Body
```
{
    "email": "nikox12@mail.ru",
    "password": "456852Zx",
}
```

###  Все примеры

#### Используя ReDoc

##### End Point
```http
        /redoc
```


#### Используя Rest API
Посмотреть\отправить запросы можно используя плагин для Visual Studia Code Rest API все примеры лежат в папке backend/request
