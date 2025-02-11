import pytest
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, all_news, home_url):
    """Количество новостей на домашней странице соответствует заданному."""
    response = client.get(home_url)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, all_news, home_url):
    """Новости отсортированы от новых к старым."""
    response = client.get(home_url)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, all_comments, news, news_url):
    """Комментарии отсортированы от старых к новым."""
    response = client.get(news_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news_url):
    """У анонимного клиента нет формы комментария."""
    response = client.get(news_url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(auth_author, news_url):
    """У авторизованного клиента есть форма комментария."""
    response = auth_author.get(news_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
