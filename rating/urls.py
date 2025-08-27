# from django.urls import path
# from .views import ArticleInteractionViewSet

# article_vote = ArticleInteractionViewSet.as_view({'patch': 'vote'})
# article_rate = ArticleInteractionViewSet.as_view({'patch': 'rate'})

# urlpatterns = [
#     path('article/<uuid:pk>/vote/', article_vote, name='article-vote'),
#     path('article/<uuid:pk>/rate/', article_rate, name='article-rate'),
# ]


from django.urls import path
from .views import ArticleVoteUpdateAPIView, ArticleRatingUpdateAPIView

urlpatterns = [
    path('api/articles/<uuid:pk>/vote/', ArticleVoteUpdateAPIView.as_view(), name='article-vote'),
    path('api/articles/<uuid:pk>/rate/', ArticleRatingUpdateAPIView.as_view(), name='article-rate'),
]


