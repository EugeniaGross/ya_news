from http import HTTPStatus

import pytest
from dateutil import parser


@pytest.mark.django_db
def test_no_auth_user(client, comment, new, data_for_comment):
    response = client.get(f'/api/v1/news/{new.id}/comment/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что GET-запрос к /api/v1/news/news_id/comment'
        'неавторизованного пользователя возращает статус 401')
    response = client.get(f'/api/v1/news/{new.id}/comment/{comment.id}/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что GET-запрос к /api/v1/news/news_id/comment/comment_id/'
        'неавторизованного пользователя возращает статус 401')
    response = client.post(
        f'/api/v1/news/{new.id}/comment/',
        data=data_for_comment
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что POST-запрос к /api/v1/news/news_id/comment'
        'неавторизованного пользователя возращает статус 401')
    response = client.delete(f'/api/v1/news/{new.id}/comment/{comment.id}/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что DELETE-запрос к /api/v1/news/news_id/comment'
        'неавторизованного пользователя возращает статус 401')
    response = client.put(
        f'/api/v1/news/{new.id}/comment/{comment.id}/',
        data=data_for_comment
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что PUT-запрос к /api/v1/news/news_id/comment'
        'неавторизованного пользователя возращает статус 401')
    response = client.patch(
        f'/api/v1/news/{new.id}/comment/{comment.id}/',
        data=data_for_comment
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Убедитесь, что PATCH-запрос к /api/v1/news/news_id/comment'
        'неавторизованного пользователя возращает статус 401')


def test_auth_user_get_request(author_client, new, comment):
    response = author_client.get(f'/api/v1/news/{new.id}/comment/')
    assert response.status_code == HTTPStatus.OK, (
        'Убедитесь, что GET-запрос к /api/v1/news/news_id/comment'
        'авторизованного пользователя возращает статус 200')
    response = author_client.get(
        f'/api/v1/news/{new.id}/comment/{comment.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Убедитесь, что GET-запрос к /api/v1/news/news_id/comment/comment_id/'
        'авторизованного пользователя возращает статус 200')


def test_auth_user_post_request(user_client, new, data_for_comment, user):
    response = user_client.post(
        f'/api/v1/news/{new.id}/comment/',
        data=data_for_comment
    )
    assert response.status_code == HTTPStatus.CREATED, (
        'Убедитесь, что POST-запрос к /api/v1/news/news_id/comment'
        'авторизованного пользователя возращает статус 201')
    assert response.json()['author'] == user.username, (
        'Убедитесь, что при создании комментария, пользователь,'
        'который отправил запрос автоматически добавляется в авторы')
    assert response.json()['text'] == data_for_comment['text'], (
        'Убедитесь, что в поле "text" добавились корректные данные')
    assert response.json()['news'] == new.id, (
        'Убедитесь, что комментарий добавлен к выбранной новости')
    assert 'created' in response.json(), (
        'Убедитесь, что при запросе создается поле "created"')
    response = user_client.post(
        f'/api/v1/news/{new.id}/comment/',
        data={}
    )
    assert response.status_code != HTTPStatus.CREATED, (
        'Убедитесь, что при передаче невалидных данных'
        'комментарий не создается')


def test_delete_request(user_client, new, comment, author_client):
    response = user_client.delete(
        f'/api/v1/news/{new.id}/comment/{comment.id}/')
    assert response.status_code == HTTPStatus.FORBIDDEN, (
        'Убедитесь, что только автор может удалять комментарий')
    response = author_client.delete(
        f'/api/v1/news/{new.id}/comment/{comment.id}/')
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        'Убедитесь, что при удалении комментария'
        'возращается статус 200')
    response = author_client.get(
        f'/api/v1/news/{new.id}/comment/{comment.id}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что комментарий удален')


def test_put_request(
        user_client,
        new,
        comment,
        author_client,
        data_for_comment,
        author
):
    response = user_client.put(
        f'/api/v1/news/{new.id}/comment/{comment.id}/',
        data=data_for_comment
    )
    assert response.status_code == HTTPStatus.FORBIDDEN, (
        'Убедитесь, что PUT-запрос к /api/v1/news/news_id/comment/comment_id/'
        'не автора комментария возращает статус 403')
    response = author_client.put(
        f'/api/v1/news/{new.id}/comment/{comment.id}/',
        data=data_for_comment
    )
    assert response.status_code == HTTPStatus.OK, (
        'Убедитесь, что PUT-запрос к /api/v1/news/news_id/comment/comment_id/'
        'автора комментария возращает статус 200')
    assert response.json()['text'] == data_for_comment['text'], (
        'Убедитесь, что изменилось поле "text"')
    assert response.json()['author'] == author.username, (
        'Убедитесь, что автор комментария не изменен'
    )
    assert response.json()['created'] != comment.created, (
        'Убедитесь, что изменилась дата публикации комментария')
    response = author_client.put(
        f'/api/v1/news/{new.id}/comment/{comment.id}/',
        data={}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        'Убедитесь, что при передаче невалидных данных'
        'комментарий не изменяется')


def test_patch_request(
    user_client,
    new, comment,
    author_client,
    data_for_comment,
    author
):
    response = user_client.patch(
        f'/api/v1/news/{new.id}/comment/{comment.id}/',
        data=data_for_comment
    )
    assert response.status_code == HTTPStatus.FORBIDDEN, (
        'Убедитесь, что PATCH-запрос к '
        '/api/v1/news/news_id/comment/comment_id/'
        'не автора комментария возращает статус 403')
    response = author_client.patch(
        f'/api/v1/news/{new.id}/comment/{comment.id}/',
        data=data_for_comment
    )
    assert response.status_code == HTTPStatus.OK, (
        'Убедитесь, что PATCH-запрос к '
        '/api/v1/news/news_id/comment/comment_id/'
        'автора комментария возращает статус 200')
    assert response.json()['text'] == data_for_comment['text'], (
        'Убедитесь, что изменилось поле "text"')
    assert response.json()['author'] == author.username, (
        'Убедитесь, что автор комментария не изменен'
    )
    assert parser.parse(response.json()['created']) == comment.created, (
        'Убедитесь, что не изменилась дата публикации комментария')
    assert response.json()['news'] == new.id, (
        'Убедитесь, что комментируемая новость не изменена')


def test_search(user_client, comment, author, new):
    response = user_client.get(
        f'/api/v1/news/{new.id}/comment/?=search={author.username}')
    assert len(response.json()) == 1, (
        'Убедитесь в правильности работы поиска по автору')
