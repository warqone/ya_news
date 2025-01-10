from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст'
    )


@pytest.fixture
def pk_for_args(news):
    return (news.pk,)


@pytest.fixture
def news_url(pk_for_args):
    return reverse('news:detail', args=pk_for_args)


@pytest.fixture
def author():
    return User.objects.create(username='Лев Толстой')


@pytest.fixture
def auth_author(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader():
    return User.objects.create(username='Читатель')


@pytest.fixture
def auth_reader(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def new_comment_text():
    return {'text': 'Новый текст'}


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def all_news():
    news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=timezone.now() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(news)


@pytest.fixture
def all_comments(news, author):
    comments = [
        Comment(
            news=news,
            text='qq',
            author=author,
            created=timezone.now() + timedelta(days=index)
        )
        for index in range(10)
    ]
    return Comment.objects.bulk_create(comments)


@pytest.fixture
def comment_form_data():
    return {'text': 'Комментарий'}
