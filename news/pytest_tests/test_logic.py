from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, comment_form_data, news_url
):
    response = client.post(news_url, data=comment_form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={news_url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(
    author, auth_author, comment_form_data, news, news_url
):
    response = auth_author.post(news_url, data=comment_form_data)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.author == author
    assert comment.news == news


@pytest.mark.django_db
@pytest.mark.parametrize('bad_words', [
    BAD_WORDS,
])
def test_user_cant_use_bad_words(auth_author, news_url, bad_words):
    bad_words_data = {'text': f'Какой-то текст, {bad_words}, еще текст'}
    response = auth_author.post(news_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_delete_comment(auth_author, news_url, delete_comment_url):
    response = auth_author.delete(delete_comment_url)
    assertRedirects(response, news_url + '#comments')
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    auth_reader, delete_comment_url
):
    response = auth_reader.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_author_can_edit_comment(
        author, auth_author, news, news_url, edit_comment_url,
        new_comment_text, comment
):
    response = auth_author.post(edit_comment_url, data=new_comment_text)
    comment = Comment.objects.get()
    assertRedirects(response, news_url + '#comments')
    assert comment.text == new_comment_text['text']
    assert comment.author == author
    assert comment.news == news


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
        auth_reader, edit_comment_url, new_comment_text, comment
):
    response = auth_reader.post(edit_comment_url, data=new_comment_text)
    comment = Comment.objects.get()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text != new_comment_text['text']
