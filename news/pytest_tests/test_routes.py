from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize('urls', [
    (pytest.lazy_fixture('home_url')),
    (pytest.lazy_fixture('news_detail_url')),
    (pytest.lazy_fixture('login_url')),
    (pytest.lazy_fixture('logout_url')),
    (pytest.lazy_fixture('signup_url')),
])
def test_pages_availability(client, urls):
    response = client.get(urls)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize('user, expected_status', [
    (pytest.lazy_fixture('auth_author'), HTTPStatus.OK),
    (pytest.lazy_fixture('auth_reader'), HTTPStatus.NOT_FOUND),
])
@pytest.mark.parametrize(
    'url', [
        (pytest.lazy_fixture('edit_comment_url')),
        (pytest.lazy_fixture('delete_comment_url')),
    ]
)
def test_availability_for_comment_edit_and_delete(
    user, expected_status, url,
):
    response = user.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    (pytest.lazy_fixture('edit_comment_url')),
    (pytest.lazy_fixture('delete_comment_url')),
])
def test_redirect_for_anonymous_client(client, url, login_url):
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
