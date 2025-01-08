import pytest
from http import HTTPStatus
from django.urls import reverse
from django.conf import settings
from pytest_django.asserts import assertRedirects

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
def test_comments_order(client, all_comments, news, pk_for_args):
    """Проверка что комментарии отсортированы от старых к новым."""
    url = reverse('news:detail', args=pk_for_args)
    response = client.get(url)
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
    client, user, expected_bool, author, reader, pk_for_args
):
    url = reverse('news:detail', args=pk_for_args)
    user_instance = author if user == 'author' else reader
    if user == 'author':
        client.force_login(user_instance)
    response = client.get(url)
    status = 'form' in response.context
    assert status == expected_bool

    # def test_anonymous_client_has_no_form(self):
    #     response = self.client.get(self.detail_url)
    #     self.assertNotIn('form', response.context)

    # def test_authorized_client_has_form(self):
    #     # Авторизуем клиент при помощи ранее созданного пользователя.
    #     self.client.force_login(self.author)
    #     response = self.client.get(self.detail_url)
    #     self.assertIn('form', response.context)
    #     # Проверим, что объект формы соответствует нужному классу формы.
    #     self.assertIsInstance(response.context['form'], CommentForm)