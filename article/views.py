from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated

from .models import Article, Comment
from .serializer import ArticleSerializer, CommentSerializer

from .permissions import IsCommentOwner


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]  # Require login for modifying actions
        return [permissions.AllowAny()]  # Allow read-only access to everyone


class ArticleCommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs['article_id'])

    def perform_create(self, serializer):
        article = Article.objects.get(pk=self.kwargs['article_id'])
        serializer.save(author=self.request.user, article=article)


class CommentUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentOwner]


