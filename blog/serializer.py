from blog.models import Article, Comment
from rest_framework import serializers
from django.contrib.auth.models import User




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    article = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'article', 'content', 'author', 'created_at']
        

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'comments', 'created_at', 'updated_at']


