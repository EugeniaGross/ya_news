from datetime import datetime, timedelta

import pytest
from django.conf import settings
from rest_framework.test import APIClient

from news.models import Comment, News


@pytest.fixture
def password():
    return 'une12345'


@pytest.fixture
def user(django_user_model, password):
    return django_user_model.objects.create_user(
        username='TestUser',
        password=password
    )


@pytest.fixture
def author(django_user_model, password):
    return django_user_model.objects.create_user(
        username='AuthorUser',
        password=password
    )


@pytest.fixture
def new():
    new = News.objects.create(title='Заголовок', text='Текст')
    return new


@pytest.fixture
def user_token(user):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
def author_token(author):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(author)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
def user_client(user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}')
    return client


@pytest.fixture
def author_client(author_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {author_token["access"]}')
    return client


@pytest.fixture
def data_for_new():
    return {
        "title": "Заголовок 1",
        "text": "Текст 1"
    }


@pytest.fixture
def data_for_new_patch():
    return {"text": "Текст 2"}


@pytest.fixture
def comment(new, author):
    return Comment.objects.create(news=new, text='Text_1', author=author)


@pytest.fixture
def data_for_comment():
    return {"text": "Text_2"}


@pytest.fixture
def news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)
