from http import HTTPStatus

import pytest
from django.conf import settings


def test_get_request(user_client, new):
    response = user_client.get('/api/v1/news/')
    assert response.status_code == HTTPStatus.OK, (
        'Проверьте, что GET-запрос к /api/v1/news/'
        'возращает ответ 200')
    assert 'text' in response.json()[0], (
        'Убедитесь, что ключ "text" содержится в ответе API')
    assert 'title' in response.json()[0], (
        'Убедитесь, что ключ "title" содержится в ответе API')
    assert 'date' in response.json()[0], (
        'Убедитесь, что ключ "text" содержится в ответе API')
    assert len(response.json()) == 1, (
        'Убедитесь, что GET-запрос к /api/v1/news/'
        'возращает тоже количество данных, что и в БД')
    response = user_client.get(f'/api/v1/news/{new.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Проверьте, что GET-запрос к /api/v1/news/'
        'возращает ответ 200')


@pytest.mark.django_db
def test_no_auth_user(client, new, data_for_new, data_for_new_patch):
    response = client.get('/api/v1/news/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что GET-запрос к /api/v1/news/'
        'неавторизованного пользователя возращает статус 401'
    )
    response = client.get(f'/api/v1/news/{new.id}/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что GET-запрос к /api/v1/news/'
        'неавторизованного пользователя возращает статус 401'
    )
    response = client.post('/api/v1/news/', data=data_for_new)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что GET-запрос к /api/v1/news/'
        'неавторизованного пользователя возращает статус 401'
    )
    response = client.delete(f'/api/v1/news/{new.id}/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что GET-запрос к /api/v1/news/'
        'неавторизованного пользователя возращает статус 401'
    )
    response = client.put('/api/v1/news/', data=data_for_new)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что GET-запрос к /api/v1/news/'
        'неавторизованного пользователя возращает статус 401'
    )
    response = client.patch('/api/v1/news/', data=data_for_new)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что GET-запрос к /api/v1/news/'
        'неавторизованного пользователя возращает статус 401'
    )


def test_post_request(user_client, data_for_new):
    response = user_client.post(
        '/api/v1/news/',
        data=data_for_new
    )
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
        'Проверьте, что POST-запрос к /api/v1/news/'
        'возращает ответ 405'
    )


def test_put_request(user_client, new, data_for_new):
    response = user_client.put(
        f'/api/v1/news/{new.id}/',
        data=data_for_new
    )
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
        'Проверьте, что PUT-запрос к /api/v1/news/'
        'возращает ответ 405'
    )


def test_delete_request(user_client, new):
    response = user_client.delete(f'/api/v1/news/{new.id}/')
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
        'Проверьте, что DELETE-запрос к /api/v1/news/'
        'возращает ответ 405'
    )


def test_patch_request(user_client, new, data_for_new_patch):
    response = user_client.patch(
        f'/api/v1/news/{new.id}/',
        data=data_for_new_patch
    )
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
        'Проверьте, что PATCH-запрос к /api/v1/news/'
        'возращает ответ 405'
    )


def test_pagination(user_client, news):
    response = user_client.get('/api/v1/news/')
    assert settings.NEWS_COUNT_ON_HOME_PAGE == len(response.json()), (
        'Убедитесь, что на странице отображается 10 запросов'
    )


def test_search(user_client, new):
    response = user_client.get(f'/api/v1/news/?search={new.title}')
    assert len(response.json()) == 1, (
        'Убедитесь, что поиск возращает правильное количество записей')
