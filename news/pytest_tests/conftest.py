from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client

from news.models import Comment, News

User = get_user_model()


@pytest.fixture  # Фикстура создания новости.
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст'
    )


@pytest.fixture  # Фикстура для получения id новости.
def pk_for_args(news):
    return (news.pk,)


@pytest.fixture  # Фикстура для создания автора коммента.
def author():
    return User.objects.create(username='Лев Толстой')

@pytest.fixture
def auth_author(author):
    client = Client()
    client.force_login(author)
    return client

@pytest.fixture  # Фикстура для создания пользователя.
def reader():
    return User.objects.create(username='Читатель')


@pytest.fixture  # Фикстура создания комментария к записи news().
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture  # Фикстура для создания 11 новостей.
def all_news():
    return [
        News.objects.create(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]


@pytest.fixture  # Фикстура для создания 10 комментариев.
def all_comments(news, author):
    return [
        Comment.objects.create(
            news=news,
            text='qq',
            author=author,
            created=datetime.now() + timedelta(days=index)
        )
        for index in range(10)
    ]
