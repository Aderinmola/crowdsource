from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from .models import Article
from .serializer import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]  # Require login for modifying actions
        return [permissions.AllowAny()]  # Allow read-only access to everyone
