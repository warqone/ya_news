import pytest
from django.urls import reverse
from django.conf import settings

HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, all_news):
    """Проверка что новостей на главной странице не больше заданного."""
    url = HOME_URL
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, all_news):
    """Проверка что новости отсортированы от свежих к старым."""
    url = HOME_URL
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, all_comments, news, news_url):
    """Проверка что комментарии отсортированы от старых к новым."""
    response = client.get(news_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
@pytest.mark.parametrize('user, expected_bool', [
    ('auth_user', True),
    ('not_auth_user', False),
])
def test_form_availability(
    client, user, expected_bool, author, reader, news_url
):
    """Проверка что форма доступна только авторизованному клиенту,
    а неавторизованному - недоступна.
    """
    user_instance = author if user == 'auth_user' else reader
    if user == 'auth_user':
        client.force_login(user_instance)
    response = client.get(news_url)
    status = 'form' in response.context
    assert status == expected_bool
