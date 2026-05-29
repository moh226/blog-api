from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Article

# Create your tests here.
class ArticleAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='alice', password='1234')
        self.user2 = User.objects.create_user(username='bob', password='1234')
        self.article = Article.objects.create(
            title='test',
            content='contenu',
            author=self.user1
        )

    def test_get_articles_public(self):
        response = self.client.get('/blog/articles/')
        assert response.status_code == 200

    def test_create_article_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/blog/articles/',
            {'title': 'nouveau', 'content': 'contenu'})
        assert response.status_code == 201

    def test_create_article_unauthenticated(self):
        response = self.client.post('/blog/articles/', {'title': 'nouveau', 'content': 'contenu'})
        print(response.status_code)
        print(response.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_article_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f'/blog/articles/{self.article.id}/',
            {'title': 'hacked', 'content': 'hacked'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_article_owner(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/blog/articles/{self.article.id}/')
        assert response.status_code == 204