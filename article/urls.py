from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet,
    ArticleCommentListCreateAPIView,
    CommentUpdateDeleteAPIView,
    )

router = DefaultRouter()
router.register(r'', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:article_id>/comments/', ArticleCommentListCreateAPIView.as_view(), name='article-comments'),
    path('comments/<uuid:pk>/', CommentUpdateDeleteAPIView.as_view(), name='comment-detail'),
]
