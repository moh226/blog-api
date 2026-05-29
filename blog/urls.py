from django.urls import include, path
from blog import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')


urlpatterns = [
    path('', include(router.urls)),
    path('articles/<int:article_pk>/comments/', views.ArticleCommentViewSet.as_view({
        'get': 'list', 'post': 'create'
        }), 
        name='article-comments'),
    path('articles/<int:article_pk>/comments/<int:pk>/', views.ArticleCommentViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
        }), 
        name='article-comment-detail'
        ),
]