# Описание проекта:
API сайта новостей YaNews, с возможностью просмотра всех новостей, отдельной новости, просмотра всех и отдельных комментариев, добавления, редактирования и удаления комментариев.

# Запуск проекта:
Клонировать репозиторий и перейти в него в командной строке

```
git clone git@github.com:EugeniaGross/ya_news.git
```

```
cd ya_news
```

Cоздать и активировать виртуальное окружение

Для Windows:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Для Linux и Mac:

```
python3 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

Выполнить миграции

Для Windows:

```
python manage.py migrate
```

Для Linux и Mac:

```
python3 manage.py migrate
```
Запустить проект

Для Windows:

```
python manage.py runserver
```

Для Linux и Mac:

```
python3 manage.py runserver
```

Для загрузки заготовленных новостей после применения миграций выполните команду:
```bash
python manage.py loaddata news.json
```
# Примеры:
Получение новости api/v1/news/{id}/
```
{
  "id": 0,
  "title": "string",
  "text": "string",
  "date": "2019-08-24"
}
```
Получение комментария api/v1/news/{news_id}/comment/{id}/
```
{
  "id": 0,
  "news": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "right": "string"
}
```
# Используемые технологии
Django, Django Rest Framework, Redoc
