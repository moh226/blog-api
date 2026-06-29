from django.shortcuts import render
from blog.models import Article, Comment
from rest_framework.response import Response
from blog.serializer import ArticleSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter




class OwnershipRequiredMixin:
    def _check_ownership(self, obj):
        if obj.author != self.request.user:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=403)
        return None




class ArticleViewSet(OwnershipRequiredMixin, ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAuthenticated()]
    
    def update(self, request, *args, **kwargs):
        article = self.get_object()
        error = self._check_ownership(article)
        if error:
            return error
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        article = self.get_object()
        error = self._check_ownership(article)
        if error:
            return error
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        error = self._check_ownership(article)
        if error:
            return error
        return super().destroy(request, *args, **kwargs)

    

    
class ArticleCommentViewSet(OwnershipRequiredMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_pk = self.kwargs.get('article_pk')
        return Comment.objects.filter(article_id=article_pk)
    

    def perform_create(self, serializer):
        article_pk = self.kwargs.get('article_pk')
        article = Article.objects.get(id=article_pk)
        serializer.save(author=self.request.user, article=article)


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAuthenticated()]
    
    
    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        error = self._check_ownership(comment)
        if error:
            return error
        return super().update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        error = self._check_ownership(comment)
        if error:
            return error
        return super().destroy(request, *args, **kwargs)