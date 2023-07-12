 
## Описание
### О проекте
Галера Яндекс практикума по поднятию навыков работы с DRF

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
python manage.py createsuperuser
```
### Наполнить базу данных:
```
python manage.py importcsv
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
POST  api/v1/users/
```
#####  Body
```
{
        "email": "paymisssr@kek.ru",
        "username": "passsymir121"
}
```
### Получение токена

##### End Point
```
POST  api/v1/auth/token/
```
#####  Body
```
{
        "username": "vdvha",
        "confirmation_code": "40041"
}
```
### Посмотреть все примеры  доступных эндпоинтов можно тут

```http
  /redoc
```
