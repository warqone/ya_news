import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, comment_form_data, news_url
):
    """Проверка что анонимный пользователь не может создать комментарий."""
    response = client.post(news_url, data=comment_form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={news_url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(
    author, auth_author, comment_form_data, news_url
):
    """Проверка что авторизованный пользователь может создать комментарий."""
    response = auth_author.post(news_url, data=comment_form_data)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.author == author


@pytest.mark.django_db
def test_user_cant_use_bad_words(auth_author, news_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = auth_author.post(news_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0
