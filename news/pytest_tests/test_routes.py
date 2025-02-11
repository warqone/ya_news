from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize('name, args', [
    ('news:home', None),
    ('news:detail', pytest.lazy_fixture('pk_for_args')),
    ('users:login', None),
    ('users:logout', None),
    ('users:signup', None),
])
def test_pages_availability(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize('user, expected_status', [
    (pytest.lazy_fixture('author'), HTTPStatus.OK),
    (pytest.lazy_fixture('reader'), HTTPStatus.NOT_FOUND),
])
@pytest.mark.parametrize(
    'name', [
        ('news:edit'),
        ('news:delete'),
    ]
)
def test_availability_for_comment_edit_and_delete(
    client, user, expected_status, name, comment
):
    client.force_login(user)
    url = reverse(name, args=(comment.pk,))
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize('name', [
    'news:edit',
    'news:delete',
])
def test_redirect_for_anonymous_client(client, name, comment):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
