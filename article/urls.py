from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet,
    ArticleCommentListCreateAPIView,
    CommentUpdateDeleteAPIView,
    )
from rating.views import ArticleVoteUpdateAPIView, ArticleRatingUpdateAPIView


# router = DefaultRouter()
# router.register(r'', ArticleViewSet, basename='article')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('<uuid:id>/', ArticleViewSet.as_view({'get': 'retrieve'}), name='article-detail'),
# ]


article_list = ArticleViewSet.as_view({
    'get': 'list',          # GET /articles/ -> list all articles
    'post': 'create'        # POST /articles/ -> create new article (login required)
})

article_detail = ArticleViewSet.as_view({
    'get': 'retrieve',      # GET /articles/<pk>/ -> get one article
    # 'put': 'update',        # PUT /articles/<pk>/ -> update article (login required)
    'patch': 'partial_update', # PATCH /articles/<pk>/ -> partial update (login required)
    'delete': 'destroy'     # DELETE /articles/<pk>/ -> delete article (login required)
})



urlpatterns = [
    # article
    path('', article_list, name='article-list'),
    path('<uuid:pk>/', article_detail, name='article-detail'),
    # rating
    path('<uuid:pk>/vote/', ArticleVoteUpdateAPIView.as_view(), name='article-vote'),
    path('<uuid:pk>/rate/', ArticleRatingUpdateAPIView.as_view(), name='article-rate'),
    # comments
    path('<uuid:article_id>/comments/', ArticleCommentListCreateAPIView.as_view(), name='article-comments'),
    path('comments/<uuid:pk>/', CommentUpdateDeleteAPIView.as_view(), name='comment-detail'),
    
]
